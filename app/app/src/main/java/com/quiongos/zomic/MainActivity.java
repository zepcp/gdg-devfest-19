package com.quiongos.zomic;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;
import android.widget.TextView;
import android.widget.RadioButton;

import com.google.gson.Gson;
import com.google.zxing.integration.android.IntentIntegrator;

import java.util.concurrent.TimeUnit;

import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.schedulers.Schedulers;
import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.adapter.rxjava2.RxJava2CallAdapterFactory;
import retrofit2.converter.gson.GsonConverterFactory;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button btn = findViewById(R.id.vote_button);
        Button qrcode = findViewById(R.id.qrcode_button);
        TextView proposal = findViewById(R.id.proposal_number);
        RadioButton voted_yes = findViewById(R.id.radio_yes);
        RadioButton voted_no = findViewById(R.id.radio_no);

        final AutoUpdateService updateService = new AutoUpdateService(makeGetRequest());

        btn.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                if (!voted_yes.isChecked() && !voted_no.isChecked()){
                    Toast.makeText(MainActivity.this, "Need an option.. ", Toast.LENGTH_SHORT).show();
                }
                else {
                    updateService.loadAutoUpdateModel(proposal.getText().toString(), voted_yes.isChecked()).subscribeOn(Schedulers.io()).observeOn(AndroidSchedulers.mainThread())
                            .doOnSuccess(response -> Toast.makeText(MainActivity.this, "BlackList: " + response.getBlackList(), Toast.LENGTH_SHORT).show()).subscribe();
                }
            }
        });

        qrcode.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                IntentIntegrator intentIntegrator = new IntentIntegrator(MainActivity.this);
                intentIntegrator.setDesiredBarcodeFormats(IntentIntegrator.QR_CODE_TYPES);
                intentIntegrator.setPrompt("Scan");
                intentIntegrator.setCameraId(0);
                intentIntegrator.setBeepEnabled(false);
                intentIntegrator.setBarcodeImageEnabled(false);
                intentIntegrator.initiateScan();
            }
        });
        handleQrCode();
    }

    private OkHttpClient getHttpClient() {
        return new OkHttpClient.Builder()
                .connectTimeout(15, TimeUnit.MINUTES)
                .readTimeout(30, TimeUnit.MINUTES)
                .writeTimeout(30, TimeUnit.MINUTES)
                .build();
    }

    private AutoUpdateService.AutoUpdateApi makeGetRequest() {
        return new Retrofit.Builder().baseUrl("https://apichain-dev.blockchainds.com")
                .client(getHttpClient())
                .addConverterFactory(GsonConverterFactory.create(new Gson()))
                .addCallAdapterFactory(RxJava2CallAdapterFactory.create())
                .build()
                .create(AutoUpdateService.AutoUpdateApi.class);


    }

    //private void openQrCodeScreen() {
    //    Integer BARCODE_READER_REQUEST_CODE = 1;

    //    Intent intent = new Intent(this, BarcodeCaptureActivity.class);
    //    startActivityForResult(intent, BARCODE_READER_REQUEST_CODE);
    //}

    private void handleQrCode() {
        (MainActivity.this).contentSubjectResult().doOnNext(result -> tryToConnect(result)).subscribe();
    }

    private void tryToConnect(String groupName) {
        nextButton.setEnabled(false);
        fragment.toggleProgressBar();
        if(groupName.equals("")) {
            fragment.showToast("Please insert a group name!");
            fragment.toggleProgressBar();
        }else {
            if (ConnectionHandler.hasNetworkConnection(fragment.getContext())) {
                Group group = new Group(groupName);
                FireBaseHandler fireBaseHandler = new FireBaseHandler(group);
                fireBaseHandler.checkAndRightGroupOnDB(false);
                handleFirebaseResponse(fireBaseHandler, group);
            } else {
                fragment.showToast("Network not available");
                fragment.toggleProgressBar();
            }
        }
        nextButton.setEnabled(true);
    }

}

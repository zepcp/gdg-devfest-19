package com.zomic.vote;


import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.google.gson.Gson;

import java.util.concurrent.TimeUnit;

import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.schedulers.Schedulers;
import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.adapter.rxjava2.RxJava2CallAdapterFactory;
import retrofit2.converter.gson.GsonConverterFactory;


public class Vote extends AppCompatActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button btn = findViewById(R.id.vote_button);
        final TextView proposal = findViewById(R.id.proposal_number);
        final RadioButton voted_yes = findViewById(R.id.radio_yes);
        final RadioButton voted_no = findViewById(R.id.radio_no);

        final PostVote updateService = new PostVote(makePostRequest());

        btn.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                if (!voted_yes.isChecked() && !voted_no.isChecked()) {
                    Toast.makeText(Vote.this, "Need an option.. ", Toast.LENGTH_SHORT).show();
                }
                else {
                    updateService.loadVoteModel(proposal.getText().toString(), voted_yes.isChecked(),
                            "0x64767925A6DF9E1ac8718AdE7b347Ea0Eb9F9d46",
                            "0xab352c099a33a5aa683e5c43655057ddb3109f5f20b4a9584175741a69d0b7e365aab3330b436e171f4552ce0d512e5fd12efaba8d2589dc2f041",
                            1575676800)
                            .subscribeOn(Schedulers.io()).observeOn(AndroidSchedulers.mainThread())
                            .doOnSuccess(response -> Toast.makeText(Vote.this, "Message: " + response.getMessage(), Toast.LENGTH_SHORT)
                                    .show()).subscribe();
                }
            }
        });
    }

    private OkHttpClient getHttpClient() {
        return new OkHttpClient.Builder()
                .connectTimeout(15, TimeUnit.MINUTES)
                .readTimeout(30, TimeUnit.MINUTES)
                .writeTimeout(30, TimeUnit.MINUTES)
                .build();
    }

    private PostVote.PostVoteApi makePostRequest() {
        return new Retrofit.Builder().baseUrl("localhost:5000")
                .client(getHttpClient())
                .addConverterFactory(GsonConverterFactory.create(new Gson()))
                .addCallAdapterFactory(RxJava2CallAdapterFactory.create())
                .build()
                .create(PostVote.PostVoteApi.class);
    }
}
package com.quiongos.zomic

import io.reactivex.Single
import retrofit2.http.GET
import retrofit2.http.Query

class AutoUpdateService(private val api: AutoUpdateApi) {

    fun loadAutoUpdateModel(proposal: String, voted_yes: Boolean): Single<AutoUpdateResponse> {
        return api.getAutoUpdateInfo(proposal, voted_yes)
    }

    interface AutoUpdateApi {

        @GET("appc/wallet_version")
        fun getAutoUpdateInfo(@Query("proposal") proposal: String, @Query("voted_yes") voted_yes: Boolean): Single<AutoUpdateResponse>

    }

}

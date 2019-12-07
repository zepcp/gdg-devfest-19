package com.zomic.vote;

import io.reactivex.Single
import retrofit2.http.Field
import retrofit2.http.POST
import retrofit2.http.Query

class PostVote(private val api: PostVoteApi) {

    fun loadVoteModel(
        proposal: String,
        voted_yes: Boolean,
        wallet: String,
        signature: String,
        time_stamp: Int
    ): Single<AutoUpdateResponse> {
        return api.postVoteInfo(proposal, voted_yes, wallet, signature, time_stamp)
    }

    interface PostVoteApi {

        @POST("/zomic/vote")
        fun postVoteInfo(@Query("proposal_id") proposal_id: String,
                         @Query("voted_yes") voted_yes: Boolean,
                         @Field("wallet") wallet: String,
                         @Field("signature") signature: String,
                         @Field("time_stamp") time_stamp: Int): Single<AutoUpdateResponse>
    }

}

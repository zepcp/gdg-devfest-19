package com.zomic.vote;

import com.google.gson.annotations.SerializedName

data class AutoUpdateResponse(@SerializedName("validator")
                              val validator: String,
                              @SerializedName("receipt")
                              val receipt: String,
                              @SerializedName("message")
                              val message: String)

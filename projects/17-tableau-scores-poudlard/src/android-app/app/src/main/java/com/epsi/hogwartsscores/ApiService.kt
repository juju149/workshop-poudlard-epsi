package com.epsi.hogwartsscores

import retrofit2.Response
import retrofit2.http.*

interface ApiService {
    
    @GET("api/houses")
    suspend fun getHouses(): Response<HousesResponse>
    
    @GET("api/houses/{id}")
    suspend fun getHouseById(@Path("id") id: Int): Response<HouseResponse>
    
    @PUT("api/houses/{id}")
    suspend fun updateHousePoints(
        @Path("id") id: Int,
        @Body request: UpdatePointsRequest
    ): Response<ApiResponse>
    
    @POST("api/houses/{id}/add")
    suspend fun addPoints(
        @Path("id") id: Int,
        @Body request: UpdatePointsRequest
    ): Response<ApiResponse>
    
    @POST("api/reset")
    suspend fun resetAllScores(): Response<ApiResponse>
    
    @GET("health")
    suspend fun healthCheck(): Response<Map<String, String>>
}

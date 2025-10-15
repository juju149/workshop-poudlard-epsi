package com.epsi.hogwartsscores

data class House(
    val id: Int,
    val name: String,
    val points: Int,
    val created_at: String? = null,
    val updated_at: String? = null
)

data class HousesResponse(
    val houses: List<House>
)

data class HouseResponse(
    val house: House
)

data class UpdatePointsRequest(
    val points: Int
)

data class ApiResponse(
    val message: String,
    val changes: Int? = null
)

data class ErrorResponse(
    val error: String
)

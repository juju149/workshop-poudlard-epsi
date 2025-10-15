package com.epsi.hogwartsscores

class HouseRepository(private val apiService: ApiService = RetrofitClient.apiService) {
    
    suspend fun getAllHouses(): Resource<List<House>> {
        return try {
            val response = apiService.getHouses()
            if (response.isSuccessful) {
                Resource.Success(response.body()?.houses ?: emptyList())
            } else {
                Resource.Error("Erreur: ${response.code()}")
            }
        } catch (e: Exception) {
            Resource.Error(e.message ?: "Erreur inconnue")
        }
    }
    
    suspend fun getHouseById(id: Int): Resource<House> {
        return try {
            val response = apiService.getHouseById(id)
            if (response.isSuccessful && response.body() != null) {
                Resource.Success(response.body()!!.house)
            } else {
                Resource.Error("Erreur: ${response.code()}")
            }
        } catch (e: Exception) {
            Resource.Error(e.message ?: "Erreur inconnue")
        }
    }
    
    suspend fun updateHousePoints(id: Int, points: Int): Resource<String> {
        return try {
            val response = apiService.updateHousePoints(id, UpdatePointsRequest(points))
            if (response.isSuccessful) {
                Resource.Success(response.body()?.message ?: "Succès")
            } else {
                Resource.Error("Erreur: ${response.code()}")
            }
        } catch (e: Exception) {
            Resource.Error(e.message ?: "Erreur inconnue")
        }
    }
    
    suspend fun addPoints(id: Int, points: Int): Resource<String> {
        return try {
            val response = apiService.addPoints(id, UpdatePointsRequest(points))
            if (response.isSuccessful) {
                Resource.Success(response.body()?.message ?: "Succès")
            } else {
                Resource.Error("Erreur: ${response.code()}")
            }
        } catch (e: Exception) {
            Resource.Error(e.message ?: "Erreur inconnue")
        }
    }
    
    suspend fun resetAllScores(): Resource<String> {
        return try {
            val response = apiService.resetAllScores()
            if (response.isSuccessful) {
                Resource.Success(response.body()?.message ?: "Succès")
            } else {
                Resource.Error("Erreur: ${response.code()}")
            }
        } catch (e: Exception) {
            Resource.Error(e.message ?: "Erreur inconnue")
        }
    }
}

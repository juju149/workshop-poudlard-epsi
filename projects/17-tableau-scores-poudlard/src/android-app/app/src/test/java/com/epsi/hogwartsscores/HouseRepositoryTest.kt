package com.epsi.hogwartsscores

import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.runTest
import org.junit.Before
import org.junit.Test
import org.junit.Assert.*
import org.mockito.kotlin.*
import retrofit2.Response

@OptIn(ExperimentalCoroutinesApi::class)
class HouseRepositoryTest {

    private lateinit var apiService: ApiService
    private lateinit var repository: HouseRepository

    @Before
    fun setup() {
        apiService = mock()
        repository = HouseRepository(apiService)
    }

    @Test
    fun `getAllHouses returns success when API call succeeds`() = runTest {
        val houses = listOf(
            House(1, "Gryffondor", 100),
            House(2, "Serpentard", 50)
        )
        val response = HousesResponse(houses)
        
        whenever(apiService.getHouses()).thenReturn(Response.success(response))
        
        val result = repository.getAllHouses()
        
        assertTrue(result is Resource.Success)
        assertEquals(2, (result as Resource.Success).data?.size)
    }

    @Test
    fun `getAllHouses returns error when API call fails`() = runTest {
        whenever(apiService.getHouses()).thenReturn(Response.error(404, mock()))
        
        val result = repository.getAllHouses()
        
        assertTrue(result is Resource.Error)
    }

    @Test
    fun `getHouseById returns success when API call succeeds`() = runTest {
        val house = House(1, "Gryffondor", 100)
        val response = HouseResponse(house)
        
        whenever(apiService.getHouseById(1)).thenReturn(Response.success(response))
        
        val result = repository.getHouseById(1)
        
        assertTrue(result is Resource.Success)
        assertEquals("Gryffondor", (result as Resource.Success).data?.name)
    }

    @Test
    fun `updateHousePoints returns success when API call succeeds`() = runTest {
        val apiResponse = ApiResponse("Success", 1)
        
        whenever(apiService.updateHousePoints(eq(1), any())).thenReturn(Response.success(apiResponse))
        
        val result = repository.updateHousePoints(1, 100)
        
        assertTrue(result is Resource.Success)
        assertEquals("Success", (result as Resource.Success).data)
    }

    @Test
    fun `addPoints returns success when API call succeeds`() = runTest {
        val apiResponse = ApiResponse("Success", 1)
        
        whenever(apiService.addPoints(eq(1), any())).thenReturn(Response.success(apiResponse))
        
        val result = repository.addPoints(1, 50)
        
        assertTrue(result is Resource.Success)
    }

    @Test
    fun `resetAllScores returns success when API call succeeds`() = runTest {
        val apiResponse = ApiResponse("All scores reset", 4)
        
        whenever(apiService.resetAllScores()).thenReturn(Response.success(apiResponse))
        
        val result = repository.resetAllScores()
        
        assertTrue(result is Resource.Success)
    }

    @Test
    fun `getAllHouses returns error when exception occurs`() = runTest {
        whenever(apiService.getHouses()).thenThrow(RuntimeException("Network error"))
        
        val result = repository.getAllHouses()
        
        assertTrue(result is Resource.Error)
        assertTrue((result as Resource.Error).message?.contains("Network error") == true)
    }
}

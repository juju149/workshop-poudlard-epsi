package com.epsi.hogwartsscores

import io.mockk.coEvery
import io.mockk.mockk
import kotlinx.coroutines.test.runTest
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import retrofit2.Response
import java.io.IOException

class HouseRepositoryTest {

    private lateinit var apiService: ApiService
    private lateinit var repository: HouseRepository

    @Before
    fun setup() {
        apiService = mockk()
        repository = HouseRepository(apiService)
    }

    @Test
    fun testGetAllHouses_Success() = runTest {
        val houses = listOf(
            House(1, "Gryffindor", 100),
            House(2, "Slytherin", 80)
        )
        val response = HousesResponse(houses)

        coEvery { apiService.getHouses() } returns Response.success(response)

        val result = repository.getAllHouses()

        assertTrue(result is Resource.Success)
        assertEquals(2, result.data?.size)
        assertEquals("Gryffindor", result.data?.get(0)?.name)
    }

    @Test
    fun testGetAllHouses_Error() = runTest {
        coEvery { apiService.getHouses() } returns Response.error(404, mockk(relaxed = true))

        val result = repository.getAllHouses()

        assertTrue(result is Resource.Error)
        assertTrue(result.message?.contains("404") == true)
    }

    @Test
    fun testGetAllHouses_Exception() = runTest {
        coEvery { apiService.getHouses() } throws IOException("Network error")

        val result = repository.getAllHouses()

        assertTrue(result is Resource.Error)
        assertEquals("Network error", result.message)
    }

    @Test
    fun testGetAllHouses_EmptyList() = runTest {
        val response = HousesResponse(emptyList())
        coEvery { apiService.getHouses() } returns Response.success(response)

        val result = repository.getAllHouses()

        assertTrue(result is Resource.Success)
        assertEquals(0, result.data?.size)
    }

    @Test
    fun testGetHouseById_Success() = runTest {
        val house = House(1, "Hufflepuff", 90)
        val response = HouseResponse(house)

        coEvery { apiService.getHouseById(1) } returns Response.success(response)

        val result = repository.getHouseById(1)

        assertTrue(result is Resource.Success)
        assertEquals("Hufflepuff", result.data?.name)
        assertEquals(90, result.data?.points)
    }

    @Test
    fun testGetHouseById_Error() = runTest {
        coEvery { apiService.getHouseById(1) } returns Response.error(500, mockk(relaxed = true))

        val result = repository.getHouseById(1)

        assertTrue(result is Resource.Error)
        assertTrue(result.message?.contains("500") == true)
    }

    @Test
    fun testGetHouseById_Exception() = runTest {
        coEvery { apiService.getHouseById(1) } throws RuntimeException("Connection timeout")

        val result = repository.getHouseById(1)

        assertTrue(result is Resource.Error)
        assertEquals("Connection timeout", result.message)
    }

    @Test
    fun testAddPoints_Success() = runTest {
        val apiResponse = ApiResponse("Points ajoutés", 1)

        coEvery { apiService.addPoints(1, UpdatePointsRequest(15)) } returns Response.success(apiResponse)

        val result = repository.addPoints(1, 15)

        assertTrue(result is Resource.Success)
        assertEquals("Points ajoutés", result.data)
    }

    @Test
    fun testAddPoints_Error() = runTest {
        coEvery { apiService.addPoints(1, UpdatePointsRequest(10)) } returns Response.error(400, mockk(relaxed = true))

        val result = repository.addPoints(1, 10)

        assertTrue(result is Resource.Error)
        assertTrue(result.message?.contains("400") == true)
    }

    @Test
    fun testAddPoints_Exception() = runTest {
        coEvery { apiService.addPoints(1, UpdatePointsRequest(10)) } throws Exception("Server error")

        val result = repository.addPoints(1, 10)

        assertTrue(result is Resource.Error)
        assertEquals("Server error", result.message)
    }

    @Test
    fun testUpdateHousePoints_Success() = runTest {
        val apiResponse = ApiResponse("Points mis à jour", 1)

        coEvery { apiService.updateHousePoints(2, UpdatePointsRequest(50)) } returns Response.success(apiResponse)

        val result = repository.updateHousePoints(2, 50)

        assertTrue(result is Resource.Success)
        assertEquals("Points mis à jour", result.data)
    }

    @Test
    fun testUpdateHousePoints_Error() = runTest {
        coEvery { apiService.updateHousePoints(2, UpdatePointsRequest(50)) } returns Response.error(403, mockk(relaxed = true))

        val result = repository.updateHousePoints(2, 50)

        assertTrue(result is Resource.Error)
        assertTrue(result.message?.contains("403") == true)
    }

    @Test
    fun testUpdateHousePoints_Exception() = runTest {
        coEvery { apiService.updateHousePoints(2, UpdatePointsRequest(50)) } throws IOException("Timeout")

        val result = repository.updateHousePoints(2, 50)

        assertTrue(result is Resource.Error)
        assertEquals("Timeout", result.message)
    }

    @Test
    fun testResetAllScores_Success() = runTest {
        val apiResponse = ApiResponse("Scores réinitialisés", 4)

        coEvery { apiService.resetAllScores() } returns Response.success(apiResponse)

        val result = repository.resetAllScores()

        assertTrue(result is Resource.Success)
        assertEquals("Scores réinitialisés", result.data)
    }

    @Test
    fun testResetAllScores_Error() = runTest {
        coEvery { apiService.resetAllScores() } returns Response.error(500, mockk(relaxed = true))

        val result = repository.resetAllScores()

        assertTrue(result is Resource.Error)
        assertTrue(result.message?.contains("500") == true)
    }

    @Test
    fun testResetAllScores_Exception() = runTest {
        coEvery { apiService.resetAllScores() } throws Exception("Database error")

        val result = repository.resetAllScores()

        assertTrue(result is Resource.Error)
        assertEquals("Database error", result.message)
    }
}

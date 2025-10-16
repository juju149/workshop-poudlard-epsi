package com.epsi.hogwartsscores

import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import io.mockk.coEvery
import io.mockk.mockk
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.setMain
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Rule
import org.junit.Test

@OptIn(ExperimentalCoroutinesApi::class)
class MainViewModelTest {

    @get:Rule
    val instantExecutorRule = InstantTaskExecutorRule()

    private val testDispatcher = UnconfinedTestDispatcher()
    private lateinit var repository: HouseRepository
    private lateinit var viewModel: MainViewModel

    @Before
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        repository = mockk()
        viewModel = MainViewModel(repository)
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun testLoadHouses_Success() {
        val houses = listOf(
            House(1, "Gryffindor", 100),
            House(2, "Slytherin", 80)
        )

        coEvery { repository.getAllHouses() } returns Resource.Success(houses)

        viewModel.loadHouses()

        val result = viewModel.houses.value
        assertTrue(result is Resource.Success)
        assertEquals(2, result?.data?.size)
    }

    @Test
    fun testLoadHouses_Error() {
        coEvery { repository.getAllHouses() } returns Resource.Error("Erreur réseau")

        viewModel.loadHouses()

        val result = viewModel.houses.value
        assertTrue(result is Resource.Error)
        assertEquals("Erreur réseau", result?.message)
    }

    @Test
    fun testLoadHouses_Loading() {
        val houses = listOf(House(1, "Ravenclaw", 70))
        coEvery { repository.getAllHouses() } returns Resource.Success(houses)

        viewModel.loadHouses()

        // Vérifie que le résultat final est Success
        val result = viewModel.houses.value
        assertTrue(result is Resource.Success)
    }

    @Test
    fun testAddPoints_Success() {
        val houses = listOf(House(1, "Gryffindor", 110))

        coEvery { repository.addPoints(1, 10) } returns Resource.Success("Points ajoutés")
        coEvery { repository.getAllHouses() } returns Resource.Success(houses)

        viewModel.addPoints(1, 10)

        val updateResult = viewModel.updateResult.value
        assertTrue(updateResult is Resource.Success)
        assertEquals("Points ajoutés", updateResult?.data)

        // Vérifie que loadHouses a été appelé
        val housesResult = viewModel.houses.value
        assertTrue(housesResult is Resource.Success)
    }

    @Test
    fun testAddPoints_Error() {
        coEvery { repository.addPoints(1, 10) } returns Resource.Error("Erreur serveur")

        viewModel.addPoints(1, 10)

        val updateResult = viewModel.updateResult.value
        assertTrue(updateResult is Resource.Error)
        assertEquals("Erreur serveur", updateResult?.message)
    }

    @Test
    fun testAddPoints_DoesNotReloadOnError() {
        coEvery { repository.addPoints(1, 10) } returns Resource.Error("Erreur")

        viewModel.addPoints(1, 10)

        // Vérifie que houses n'a pas été rechargé après une erreur
        val housesResult = viewModel.houses.value
        assertNull(housesResult)
    }

    @Test
    fun testUpdatePoints_Success() {
        val houses = listOf(House(2, "Slytherin", 50))

        coEvery { repository.updateHousePoints(2, 50) } returns Resource.Success("Points mis à jour")
        coEvery { repository.getAllHouses() } returns Resource.Success(houses)

        viewModel.updatePoints(2, 50)

        val updateResult = viewModel.updateResult.value
        assertTrue(updateResult is Resource.Success)
        assertEquals("Points mis à jour", updateResult?.data)

        // Vérifie le rechargement
        val housesResult = viewModel.houses.value
        assertTrue(housesResult is Resource.Success)
    }

    @Test
    fun testUpdatePoints_Error() {
        coEvery { repository.updateHousePoints(2, 50) } returns Resource.Error("Forbidden")

        viewModel.updatePoints(2, 50)

        val updateResult = viewModel.updateResult.value
        assertTrue(updateResult is Resource.Error)
        assertEquals("Forbidden", updateResult?.message)
    }

    @Test
    fun testResetScores_Success() {
        val houses = listOf(
            House(1, "Gryffindor", 0),
            House(2, "Slytherin", 0)
        )

        coEvery { repository.resetAllScores() } returns Resource.Success("Scores réinitialisés")
        coEvery { repository.getAllHouses() } returns Resource.Success(houses)

        viewModel.resetScores()

        val updateResult = viewModel.updateResult.value
        assertTrue(updateResult is Resource.Success)
        assertEquals("Scores réinitialisés", updateResult?.data)

        // Vérifie le rechargement
        val housesResult = viewModel.houses.value
        assertTrue(housesResult is Resource.Success)
        assertEquals(2, housesResult?.data?.size)
    }

    @Test
    fun testResetScores_Error() {
        coEvery { repository.resetAllScores() } returns Resource.Error("Permission denied")

        viewModel.resetScores()

        val updateResult = viewModel.updateResult.value
        assertTrue(updateResult is Resource.Error)
        assertEquals("Permission denied", updateResult?.message)
    }
}

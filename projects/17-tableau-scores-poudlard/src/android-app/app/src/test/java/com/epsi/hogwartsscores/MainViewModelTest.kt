package com.epsi.hogwartsscores

import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.*
import org.junit.After
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.junit.Assert.*
import org.mockito.kotlin.*

@OptIn(ExperimentalCoroutinesApi::class)
class MainViewModelTest {

    @get:Rule
    val instantExecutorRule = InstantTaskExecutorRule()

    private val testDispatcher = StandardTestDispatcher()
    private lateinit var repository: HouseRepository
    private lateinit var viewModel: MainViewModel

    @Before
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        repository = mock()
        viewModel = MainViewModel(repository)
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun `loadHouses updates houses LiveData with success`() = runTest {
        val houses = listOf(
            House(1, "Gryffondor", 100),
            House(2, "Serpentard", 50)
        )
        
        whenever(repository.getAllHouses()).thenReturn(Resource.Success(houses))
        
        viewModel.loadHouses()
        testDispatcher.scheduler.advanceUntilIdle()
        
        val result = viewModel.houses.value
        assertTrue(result is Resource.Success)
        assertEquals(2, (result as Resource.Success).data?.size)
    }

    @Test
    fun `loadHouses updates houses LiveData with error`() = runTest {
        whenever(repository.getAllHouses()).thenReturn(Resource.Error("Network error"))
        
        viewModel.loadHouses()
        testDispatcher.scheduler.advanceUntilIdle()
        
        val result = viewModel.houses.value
        assertTrue(result is Resource.Error)
    }

    @Test
    fun `addPoints calls repository and reloads houses on success`() = runTest {
        val houses = listOf(House(1, "Gryffondor", 150))
        
        whenever(repository.addPoints(1, 50)).thenReturn(Resource.Success("Success"))
        whenever(repository.getAllHouses()).thenReturn(Resource.Success(houses))
        
        viewModel.addPoints(1, 50)
        testDispatcher.scheduler.advanceUntilIdle()
        
        verify(repository).addPoints(1, 50)
        verify(repository, atLeastOnce()).getAllHouses()
    }

    @Test
    fun `updatePoints calls repository and reloads houses on success`() = runTest {
        val houses = listOf(House(1, "Gryffondor", 100))
        
        whenever(repository.updateHousePoints(1, 100)).thenReturn(Resource.Success("Success"))
        whenever(repository.getAllHouses()).thenReturn(Resource.Success(houses))
        
        viewModel.updatePoints(1, 100)
        testDispatcher.scheduler.advanceUntilIdle()
        
        verify(repository).updateHousePoints(1, 100)
        verify(repository, atLeastOnce()).getAllHouses()
    }

    @Test
    fun `resetScores calls repository and reloads houses on success`() = runTest {
        val houses = listOf(
            House(1, "Gryffondor", 0),
            House(2, "Serpentard", 0)
        )
        
        whenever(repository.resetAllScores()).thenReturn(Resource.Success("Success"))
        whenever(repository.getAllHouses()).thenReturn(Resource.Success(houses))
        
        viewModel.resetScores()
        testDispatcher.scheduler.advanceUntilIdle()
        
        verify(repository).resetAllScores()
        verify(repository, atLeastOnce()).getAllHouses()
    }

    @Test
    fun `addPoints does not reload houses on error`() = runTest {
        whenever(repository.addPoints(1, 50)).thenReturn(Resource.Error("Error"))
        
        viewModel.addPoints(1, 50)
        testDispatcher.scheduler.advanceUntilIdle()
        
        verify(repository).addPoints(1, 50)
        verify(repository, never()).getAllHouses()
    }
}

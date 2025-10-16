package com.epsi.hogwartsscores

import org.junit.Assert.*
import org.junit.Test

class MainViewModelTest {
    @Test
    fun testInitialScoreIsZero() {
        val viewModel = MainViewModel()
        assertEquals(0, viewModel.getScore("Gryffindor"))
    }

    @Test
    fun testAddScore() {
        val viewModel = MainViewModel()
        viewModel.addScore("Gryffindor", 10)
        assertEquals(10, viewModel.getScore("Gryffindor"))
    }

    @Test
    fun testMultipleHouses() {
        val viewModel = MainViewModel()
        viewModel.addScore("Gryffindor", 10)
        viewModel.addScore("Slytherin", 5)
        assertEquals(10, viewModel.getScore("Gryffindor"))
        assertEquals(5, viewModel.getScore("Slytherin"))
    }
}

package com.epsi.hogwartsscores

import org.junit.Assert.*
import org.junit.Test

class HouseRepositoryTest {
    @Test
    fun testAddHouse() {
        val repo = HouseRepository()
        repo.addHouse("Ravenclaw")
        assertTrue(repo.getHouses().contains("Ravenclaw"))
    }

    @Test
    fun testAddScoreToHouse() {
        val repo = HouseRepository()
        repo.addHouse("Hufflepuff")
        repo.addScore("Hufflepuff", 15)
        assertEquals(15, repo.getScore("Hufflepuff"))
    }
}

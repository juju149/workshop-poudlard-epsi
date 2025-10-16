package com.epsi.hogwartsscores

import org.junit.Assert.*
import org.junit.Test

class ApiServiceTest {
    @Test
    fun testApiReturnsScores() {
        val api = ApiService()
        val scores = api.getScores()
        assertNotNull(scores)
        assertTrue(scores.isNotEmpty())
    }
}

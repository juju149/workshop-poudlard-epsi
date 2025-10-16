package com.epsi.hogwartsscores

import org.junit.Assert.*
import org.junit.Test

class ApiServiceTest {
    @Test
    fun testApiServiceIsNotNull() {
        val api = RetrofitClient.apiService
        assertNotNull(api)
    }
}

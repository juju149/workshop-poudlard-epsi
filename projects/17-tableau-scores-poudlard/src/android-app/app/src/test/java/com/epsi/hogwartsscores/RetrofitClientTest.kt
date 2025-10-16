package com.epsi.hogwartsscores

import org.junit.Assert.*
import org.junit.Test

class RetrofitClientTest {
    @Test
    fun testRetrofitApiServiceIsNotNull() {
        val apiService = RetrofitClient.apiService
        assertNotNull(apiService)
    }
}

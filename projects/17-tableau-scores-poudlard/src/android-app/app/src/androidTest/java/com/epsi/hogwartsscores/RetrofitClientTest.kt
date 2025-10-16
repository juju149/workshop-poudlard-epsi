package com.epsi.hogwartsscores

import org.junit.Assert.*
import org.junit.Test

class RetrofitClientTest {
    @Test
    fun testRetrofitInstance() {
        val client = RetrofitClient.getInstance()
        assertNotNull(client)
    }
}

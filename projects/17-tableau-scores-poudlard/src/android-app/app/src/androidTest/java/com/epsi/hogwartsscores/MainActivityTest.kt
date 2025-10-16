package com.epsi.hogwartsscores

import org.junit.Assert.*
import org.junit.Test

class MainActivityTest {
    @Test
    fun testActivityLaunch() {
        val activity = MainActivity()
        assertNotNull(activity)
    }
}

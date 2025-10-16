package com.epsi.hogwartsscores

import org.junit.Assert.*
import org.junit.Test

class ModelsTest {
    @Test
    fun testHouseModel() {
        val house = House("Gryffindor", 0)
        assertEquals("Gryffindor", house.name)
        assertEquals(0, house.score)
    }
}

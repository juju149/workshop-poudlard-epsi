package com.epsi.hogwartsscores

import org.junit.Test
import org.junit.Assert.*

class ResourceTest {

    @Test
    fun `Success resource should contain data`() {
        val data = listOf(House(1, "Gryffondor", 100))
        val resource = Resource.Success(data)
        
        assertNotNull(resource.data)
        assertEquals(1, resource.data?.size)
        assertEquals("Gryffondor", resource.data?.get(0)?.name)
    }

    @Test
    fun `Error resource should contain message`() {
        val resource = Resource.Error<List<House>>("Network error")
        
        assertNull(resource.data)
        assertEquals("Network error", resource.message)
    }

    @Test
    fun `Loading resource should have no data or message`() {
        val resource = Resource.Loading<List<House>>()
        
        assertNull(resource.data)
        assertNull(resource.message)
    }

    @Test
    fun `Error resource can contain partial data`() {
        val data = listOf(House(1, "Gryffondor", 100))
        val resource = Resource.Error("Partial error", data)
        
        assertNotNull(resource.data)
        assertEquals("Partial error", resource.message)
    }
}

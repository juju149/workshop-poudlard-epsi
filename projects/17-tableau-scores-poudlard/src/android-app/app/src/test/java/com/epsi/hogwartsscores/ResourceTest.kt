package com.epsi.hogwartsscores

import org.junit.Assert.*
import org.junit.Test

class ResourceTest {

    @Test
    fun testResourceSuccess() {
        val data = "Test data"
        val resource = Resource.Success(data)

        assertEquals(data, resource.data)
        assertNull(resource.message)
        assertTrue(resource is Resource.Success)
    }

    @Test
    fun testResourceError_WithMessage() {
        val errorMessage = "Test error"
        val resource = Resource.Error<String>(errorMessage)

        assertEquals(errorMessage, resource.message)
        assertNull(resource.data)
        assertTrue(resource is Resource.Error)
    }

    @Test
    fun testResourceError_WithData() {
        val errorMessage = "Test error"
        val data = "Partial data"
        val resource = Resource.Error(errorMessage, data)

        assertEquals(errorMessage, resource.message)
        assertEquals(data, resource.data)
        assertTrue(resource is Resource.Error)
    }

    @Test
    fun testResourceLoading() {
        val resource = Resource.Loading<String>()

        assertNull(resource.data)
        assertNull(resource.message)
        assertTrue(resource is Resource.Loading)
    }

    @Test
    fun testResourceSuccess_WithList() {
        val houses = listOf(
            House(1, "Gryffindor", 100),
            House(2, "Slytherin", 80)
        )
        val resource = Resource.Success(houses)

        assertEquals(2, resource.data?.size)
        assertEquals("Gryffindor", resource.data?.get(0)?.name)
    }

    @Test
    fun testResourceError_WithNullData() {
        val resource = Resource.Error<String>("Error", null)

        assertEquals("Error", resource.message)
        assertNull(resource.data)
    }
}


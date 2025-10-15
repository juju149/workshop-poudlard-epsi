package com.epsi.hogwartsscores

import org.junit.Test
import org.junit.Assert.*

class ModelsTest {

    @Test
    fun `House should have correct properties`() {
        val house = House(
            id = 1,
            name = "Gryffondor",
            points = 100
        )
        
        assertEquals(1, house.id)
        assertEquals("Gryffondor", house.name)
        assertEquals(100, house.points)
    }

    @Test
    fun `UpdatePointsRequest should have correct points value`() {
        val request = UpdatePointsRequest(50)
        assertEquals(50, request.points)
    }

    @Test
    fun `ApiResponse should have correct message`() {
        val response = ApiResponse("Success", 1)
        assertEquals("Success", response.message)
        assertEquals(1, response.changes)
    }

    @Test
    fun `HousesResponse should contain list of houses`() {
        val houses = listOf(
            House(1, "Gryffondor", 100),
            House(2, "Serpentard", 50)
        )
        val response = HousesResponse(houses)
        
        assertEquals(2, response.houses.size)
        assertEquals("Gryffondor", response.houses[0].name)
    }
}

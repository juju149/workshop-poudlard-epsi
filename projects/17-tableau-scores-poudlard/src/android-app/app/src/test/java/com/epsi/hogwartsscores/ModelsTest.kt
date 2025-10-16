package com.epsi.hogwartsscores

import org.junit.Assert.*
import org.junit.Test

class ModelsTest {
    @Test
    fun testHouseModel() {
        val house = House(
            id = 1,
            name = "Gryffindor",
            points = 100,
            created_at = "2024-01-01",
            updated_at = "2024-01-01"
        )
        assertEquals(1, house.id)
        assertEquals("Gryffindor", house.name)
        assertEquals(100, house.points)
    }

    @Test
    fun testHouseModelWithNullDates() {
        val house = House(
            id = 2,
            name = "Slytherin",
            points = 50
        )
        assertEquals(2, house.id)
        assertEquals("Slytherin", house.name)
        assertEquals(50, house.points)
        assertNull(house.created_at)
        assertNull(house.updated_at)
    }

    @Test
    fun testHousesResponse() {
        val houses = listOf(
            House(1, "Gryffindor", 100),
            House(2, "Slytherin", 80),
            House(3, "Ravenclaw", 90),
            House(4, "Hufflepuff", 70)
        )
        val response = HousesResponse(houses)

        assertEquals(4, response.houses.size)
        assertEquals("Gryffindor", response.houses[0].name)
        assertEquals(80, response.houses[1].points)
    }

    @Test
    fun testHouseResponse() {
        val house = House(1, "Ravenclaw", 90)
        val response = HouseResponse(house)

        assertEquals(1, response.house.id)
        assertEquals("Ravenclaw", response.house.name)
        assertEquals(90, response.house.points)
    }

    @Test
    fun testUpdatePointsRequest() {
        val request = UpdatePointsRequest(25)

        assertEquals(25, request.points)
    }

    @Test
    fun testUpdatePointsRequest_NegativePoints() {
        val request = UpdatePointsRequest(-10)

        assertEquals(-10, request.points)
    }

    @Test
    fun testApiResponse() {
        val response = ApiResponse("Success", 1)

        assertEquals("Success", response.message)
        assertEquals(1, response.changes)
    }

    @Test
    fun testApiResponse_WithoutChanges() {
        val response = ApiResponse("Operation completed")

        assertEquals("Operation completed", response.message)
        assertNull(response.changes)
    }

    @Test
    fun testErrorResponse() {
        val errorResponse = ErrorResponse("Invalid request")

        assertEquals("Invalid request", errorResponse.error)
    }

    @Test
    fun testHouseEquality() {
        val house1 = House(1, "Gryffindor", 100)
        val house2 = House(1, "Gryffindor", 100)

        assertEquals(house1, house2)
    }

    @Test
    fun testHouseCopy() {
        val house1 = House(1, "Hufflepuff", 60)
        val house2 = house1.copy(points = 70)

        assertEquals(1, house2.id)
        assertEquals("Hufflepuff", house2.name)
        assertEquals(70, house2.points)
    }
}

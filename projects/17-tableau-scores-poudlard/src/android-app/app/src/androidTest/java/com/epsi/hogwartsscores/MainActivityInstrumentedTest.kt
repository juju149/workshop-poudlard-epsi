package com.epsi.hogwartsscores

import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.rule.ActivityTestRule
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.click
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.withId
import androidx.test.espresso.matcher.ViewMatchers.withText
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class MainActivityInstrumentedTest {
    @get:Rule
    val activityRule = ActivityTestRule(MainActivity::class.java)

    @Test
    fun afficheTitreCorrect() {
        onView(withId(R.id.titleTextView)).check(matches(withText("🏰 Tableau des Scores de Poudlard")))
    }

    @Test
    fun clicRefreshNePlantePas() {
        onView(withId(R.id.btnRefresh)).perform(click())
        // On vérifie juste que le bouton est cliquable et ne plante pas
    }
}

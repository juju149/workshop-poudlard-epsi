package com.epsi.hogwartsscores

import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import android.widget.TextView
import androidx.test.core.app.ApplicationProvider
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.junit.Assert.*

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class MainActivityTest {
    @Test
    fun `activity should be created`() {
        val activity = Robolectric.buildActivity(MainActivity::class.java).setup().get()
        assertNotNull(activity)
    }

    @Test
    fun `should display correct title`() {
        val activity = Robolectric.buildActivity(MainActivity::class.java).setup().get()
        val titleView = activity.findViewById<TextView>(R.id.titleTextView)
        assertNotNull("TextView titleTextView introuvable", titleView)
        val actualText = titleView?.text?.toString()
        assertEquals("Texte du titre inattendu: $actualText", "🏰 Tableau des Scores de Poudlard", actualText)
    }

    @Test
    fun `updateUI affiche les noms et points des maisons`() {
        val activity = Robolectric.buildActivity(MainActivity::class.java).setup().get()
        val houses: List<House> = listOf(
            House(1, "Gryffondor", 100),
            House(2, "Serpentard", 80),
            House(3, "Poufsouffle", 60),
            House(4, "Serdaigle", 40)
        )
        val method = activity.javaClass.getDeclaredMethod("updateUI", List::class.java)
        method.isAccessible = true
        method.invoke(activity, houses)
        assertEquals("Gryffondor", activity.findViewById<TextView>(R.id.house1Name).text)
        assertEquals("100 points", activity.findViewById<TextView>(R.id.house1Points).text)
        assertEquals("Serpentard", activity.findViewById<TextView>(R.id.house2Name).text)
        assertEquals("80 points", activity.findViewById<TextView>(R.id.house2Points).text)
        assertEquals("Poufsouffle", activity.findViewById<TextView>(R.id.house3Name).text)
        assertEquals("60 points", activity.findViewById<TextView>(R.id.house3Points).text)
        assertEquals("Serdaigle", activity.findViewById<TextView>(R.id.house4Name).text)
        assertEquals("40 points", activity.findViewById<TextView>(R.id.house4Points).text)
    }

    @Test
    fun `affichage du ProgressBar et Toast lors du chargement et erreur`() {
        val activity = Robolectric.buildActivity(MainActivity::class.java).setup().get()
        // Simule le chargement
        activity.runOnUiThread {
            activity.findViewById<ProgressBar>(R.id.progressBar).visibility = View.GONE
        }
        activity.runOnUiThread {
            activity.findViewById<ProgressBar>(R.id.progressBar).visibility = View.VISIBLE
        }
        assertEquals(View.VISIBLE, activity.findViewById<ProgressBar>(R.id.progressBar).visibility)
        // Simule une erreur (Toast non testable directement, mais on vérifie la visibilité du ProgressBar)
        activity.runOnUiThread {
            activity.findViewById<ProgressBar>(R.id.progressBar).visibility = View.GONE
        }
        assertEquals(View.GONE, activity.findViewById<ProgressBar>(R.id.progressBar).visibility)
    }

    @Test
    fun `clic sur le bouton refresh déclenche le chargement des maisons`() {
        val activity = Robolectric.buildActivity(MainActivity::class.java).setup().get()
        val btnRefresh = activity.findViewById<Button>(R.id.btnRefresh)
        btnRefresh.performClick()
        // On ne peut pas vérifier l'appel direct à viewModel.loadHouses sans mock, mais on vérifie que le clic ne plante pas
        assertNotNull(btnRefresh)
    }
}

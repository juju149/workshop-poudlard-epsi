package com.epsi.hogwartsscores

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import com.google.android.material.textfield.TextInputEditText

class MainActivity : AppCompatActivity() {
    
    private lateinit var viewModel: MainViewModel
    private lateinit var progressBar: ProgressBar
    private lateinit var house1Name: TextView
    private lateinit var house1Points: TextView
    private lateinit var house2Name: TextView
    private lateinit var house2Points: TextView
    private lateinit var house3Name: TextView
    private lateinit var house3Points: TextView
    private lateinit var house4Name: TextView
    private lateinit var house4Points: TextView
    private lateinit var btnRefresh: Button
    private lateinit var btnReset: Button
    
    private var houses: List<House> = emptyList()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        viewModel = ViewModelProvider(this)[MainViewModel::class.java]
        
        initViews()
        setupObservers()
        setupListeners()
        
        viewModel.loadHouses()
    }
    
    private fun initViews() {
        progressBar = findViewById(R.id.progressBar)
        house1Name = findViewById(R.id.house1Name)
        house1Points = findViewById(R.id.house1Points)
        house2Name = findViewById(R.id.house2Name)
        house2Points = findViewById(R.id.house2Points)
        house3Name = findViewById(R.id.house3Name)
        house3Points = findViewById(R.id.house3Points)
        house4Name = findViewById(R.id.house4Name)
        house4Points = findViewById(R.id.house4Points)
        btnRefresh = findViewById(R.id.btnRefresh)
        btnReset = findViewById(R.id.btnReset)
    }
    
    private fun setupObservers() {
        viewModel.houses.observe(this) { resource ->
            when (resource) {
                is Resource.Loading -> {
                    progressBar.visibility = View.VISIBLE
                }
                is Resource.Success -> {
                    progressBar.visibility = View.GONE
                    resource.data?.let { updateUI(it) }
                }
                is Resource.Error -> {
                    progressBar.visibility = View.GONE
                    Toast.makeText(this, "Erreur: ${resource.message}", Toast.LENGTH_LONG).show()
                }
            }
        }
        
        viewModel.updateResult.observe(this) { resource ->
            when (resource) {
                is Resource.Success -> {
                    Toast.makeText(this, resource.data, Toast.LENGTH_SHORT).show()
                }
                is Resource.Error -> {
                    Toast.makeText(this, "Erreur: ${resource.message}", Toast.LENGTH_LONG).show()
                }
                is Resource.Loading -> {
                    // Géré par houses observer
                }
            }
        }
    }
    
    private fun setupListeners() {
        btnRefresh.setOnClickListener {
            viewModel.loadHouses()
        }
        
        btnReset.setOnClickListener {
            showResetConfirmationDialog()
        }
        
        findViewById<Button>(R.id.btnAddHouse1).setOnClickListener {
            if (houses.isNotEmpty()) showAddPointsDialog(houses[0])
        }
        
        findViewById<Button>(R.id.btnAddHouse2).setOnClickListener {
            if (houses.size > 1) showAddPointsDialog(houses[1])
        }
        
        findViewById<Button>(R.id.btnAddHouse3).setOnClickListener {
            if (houses.size > 2) showAddPointsDialog(houses[2])
        }
        
        findViewById<Button>(R.id.btnAddHouse4).setOnClickListener {
            if (houses.size > 3) showAddPointsDialog(houses[3])
        }
    }
    
    private fun updateUI(housesList: List<House>) {
        houses = housesList
        
        if (housesList.isNotEmpty()) {
            house1Name.text = housesList[0].name
            house1Points.text = "${housesList[0].points} points"
        }
        
        if (housesList.size > 1) {
            house2Name.text = housesList[1].name
            house2Points.text = "${housesList[1].points} points"
        }
        
        if (housesList.size > 2) {
            house3Name.text = housesList[2].name
            house3Points.text = "${housesList[2].points} points"
        }
        
        if (housesList.size > 3) {
            house4Name.text = housesList[3].name
            house4Points.text = "${housesList[3].points} points"
        }
    }
    
    private fun showAddPointsDialog(house: House) {
        val dialogView = layoutInflater.inflate(R.layout.dialog_add_points, null)
        val inputPoints = dialogView.findViewById<TextInputEditText>(R.id.inputPoints)
        
        AlertDialog.Builder(this)
            .setTitle("Ajouter/Retirer des points")
            .setMessage("Maison: ${house.name}\nPoints actuels: ${house.points}")
            .setView(dialogView)
            .setPositiveButton("Ajouter") { _, _ ->
                val points = inputPoints.text.toString().toIntOrNull()
                if (points != null) {
                    viewModel.addPoints(house.id, points)
                } else {
                    Toast.makeText(this, "Valeur invalide", Toast.LENGTH_SHORT).show()
                }
            }
            .setNegativeButton("Annuler", null)
            .show()
    }
    
    private fun showResetConfirmationDialog() {
        AlertDialog.Builder(this)
            .setTitle("Réinitialiser les scores")
            .setMessage("Êtes-vous sûr de vouloir réinitialiser tous les scores à 0 ?")
            .setPositiveButton("Oui") { _, _ ->
                viewModel.resetScores()
            }
            .setNegativeButton("Non", null)
            .show()
    }
}

package com.epsi.hogwartsscores

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch

class MainViewModel(private val repository: HouseRepository = HouseRepository()) : ViewModel() {
    
    private val _houses = MutableLiveData<Resource<List<House>>>()
    val houses: LiveData<Resource<List<House>>> = _houses
    
    private val _updateResult = MutableLiveData<Resource<String>>()
    val updateResult: LiveData<Resource<String>> = _updateResult
    
    fun loadHouses() {
        viewModelScope.launch {
            _houses.value = Resource.Loading()
            _houses.value = repository.getAllHouses()
        }
    }
    
    fun addPoints(houseId: Int, points: Int) {
        viewModelScope.launch {
            _updateResult.value = Resource.Loading()
            _updateResult.value = repository.addPoints(houseId, points)
            if (_updateResult.value is Resource.Success) {
                loadHouses()
            }
        }
    }
    
    fun updatePoints(houseId: Int, points: Int) {
        viewModelScope.launch {
            _updateResult.value = Resource.Loading()
            _updateResult.value = repository.updateHousePoints(houseId, points)
            if (_updateResult.value is Resource.Success) {
                loadHouses()
            }
        }
    }
    
    fun resetScores() {
        viewModelScope.launch {
            _updateResult.value = Resource.Loading()
            _updateResult.value = repository.resetAllScores()
            if (_updateResult.value is Resource.Success) {
                loadHouses()
            }
        }
    }
}

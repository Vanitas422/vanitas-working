package com.example.vawrok

import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.ListView
import androidx.appcompat.app.AppCompatActivity

class ListActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_list)

        val listView: ListView = findViewById(R.id.lv_data)
        val items = listOf(
            "Kotlin",
            "Android Studio",
            "RecyclerView",
            "ViewBinding",
            "Material Design",
            "Gradle"
        )

        val adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, items)
        listView.adapter = adapter
    }
}

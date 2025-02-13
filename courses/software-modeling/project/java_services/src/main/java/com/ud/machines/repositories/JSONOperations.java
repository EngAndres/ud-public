/**
 * This class is responsible for all the JSON operations that are needed in the project.
 * 
 * Author: Carlos Andres Sierra <casierrav@udistrital.edu.co>
 */

 package com.example.condor.repositories;

 import java.io.File;
 import java.io.FileWriter;
 import java.io.IOException;
 import java.io.InputStream;
 import java.lang.reflect.Field;
 import java.nio.charset.StandardCharsets;
 import java.util.ArrayList;
 import java.util.List;
 
 import org.json.JSONArray;
import org.json.JSONException;
 import org.json.JSONObject;
 
 /**
  * This class is responsible for all the JSON operations that are needed in the project.
  */
 public class JSONOperations {
 
    /**
     * This method loads data from a JSON file and returns a list of objects of the specified class.
     * @param <T>
     * @param filePath
     * @param clazz
     * @return a list of objects of the specified class
     */
    public static <T> List<T> loadData(String filePath, Class<T> clazz) {
        List<T> objects = new ArrayList<>();
        try (InputStream inputStream = JSONOperations.class.getClassLoader().getResourceAsStream(filePath)) {
            if (inputStream == null) {
                 throw new IOException("File not found: " + filePath);
            }
             
            String content = new String(inputStream.readAllBytes(), StandardCharsets.UTF_8);
            JSONArray jsonArray = new JSONArray(content);
            
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject jsonObject = jsonArray.getJSONObject(i);
                T obj = clazz.getDeclaredConstructor().newInstance();
                for (Field field : clazz.getDeclaredFields()) {
                    field.setAccessible(true);
                    String fieldName = field.getName();
                    
                    if (jsonObject.has(fieldName)) {
                        Object value = jsonObject.get(fieldName);
                        if (field.getType().isAssignableFrom(value.getClass())) {
                            field.set(obj, value);
                        } else if (field.getType() == int.class && value instanceof Number) {
                            field.set(obj, ((Number) value).intValue());
                        } else if (field.getType() == double.class && value instanceof Number) {
                            field.set(obj, ((Number) value).doubleValue());
                        } else if (field.getType() == long.class && value instanceof Number) {
                            field.set(obj, ((Number) value).longValue());
                        } else if (field.getType() == boolean.class && value instanceof Boolean) {
                            field.set(obj, value);
                        } else if (field.getType() == String.class && value instanceof String) {
                            field.set(obj, value);
                        }
                    }
                }
                objects.add(obj);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return objects;
    }

    /**
     * This method saves data to a JSON file.
     * @param <T>
     * @param filePath
     * @param objects
     */
    public static <T> void saveData(String filePath, List<T> objects) {
        JSONArray jsonArray = new JSONArray();
        try {
            filePath = "src/main/resources/" + filePath;
            for (T obj : objects) {
                JSONObject jsonObject = new JSONObject();
                for (Field field : obj.getClass().getDeclaredFields()) {
                    field.setAccessible(true);
                    jsonObject.put(field.getName(), field.get(obj));
                }
                jsonArray.put(jsonObject);
            }
            
            try (FileWriter fileWriter = new FileWriter(filePath)) {
                fileWriter.write(jsonArray.toString(4)); // Pretty print with an indent factor of 4
            }
        } catch (IOException | IllegalAccessException | IllegalArgumentException | SecurityException | JSONException e) {
            e.printStackTrace();
        }
    }
}
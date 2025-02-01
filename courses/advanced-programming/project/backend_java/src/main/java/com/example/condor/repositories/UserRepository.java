/**
 * This file has a class to handle user data.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co?
 */

package com.example.condor.repositories;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import javax.annotation.PostConstruct;

import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.stereotype.Repository;

import com.example.condor.data_objects.AuthData;
import com.example.condor.data_objects.UserData;

@Repository
public class UserRepository {

    private List<UserData> users = new ArrayList<>();

    @PostConstruct
    public void init(){
        this.loadData();
    }

    private void loadData() {
        String filePath = "data/users.json";
        try (InputStream inputStream = getClass().getClassLoader().getResourceAsStream(filePath)) {
            if (inputStream == null) {
                throw new IOException("File not found: " + filePath);
            }
            String content = new String(inputStream.readAllBytes(), StandardCharsets.UTF_8);
            JSONArray jsonArray = new JSONArray(content);
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject jsonObject = jsonArray.getJSONObject(i);
                UserData user = new UserData(
                        jsonObject.getInt("id"),
                        jsonObject.getString("name"),
                        jsonObject.getString("username"),
                        jsonObject.getString("password"),
                        jsonObject.getString("language"),
                        jsonObject.getString("location"),
                        jsonObject.getInt("age")
                );
                this.users.add(user);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * This method is used to get a user by the id.
     *
     * @param id
     * @return user information
     */
    public Optional<UserData> getUserById(int id) {
        for(UserData user : this.users) {
            if(user.id == id) 
                return Optional.of(user);
        }
        return Optional.empty();
    }

    /**
     * This method is used to authenticate an user in the application.
     *
     * @param authData
     * @return An object with user data if it is authenticated.
     */
    public Optional<UserData> authUser(AuthData authData) {
        for(UserData user : this.users) {
            if (user.username.equals(authData.username) && user.password.equals(authData.password)) {
                return Optional.of(user);
            }
        }
        return Optional.empty();
    }

    /**
     * This method is used to add a new user in the application.
     *
     * @param userData
     * @return An object with user data.
     */
    public UserData addUser(UserData userData) {
        int last_id = -1;
        for(UserData user : this.users) {
            if (user.id > last_id) {
                last_id = user.id;
            }
        }
        userData.id = last_id + 1;
        this.users.add(userData);
        return userData;
    }
    
}

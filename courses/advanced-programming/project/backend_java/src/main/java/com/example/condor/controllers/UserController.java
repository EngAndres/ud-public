/*
 * This is a class to handle web services
 * related to user functionalities.
 * 
 * Author: Carlos Andres Sierra <casierrav@udistrital.edu.co>
 */
package com.example.condor.controllers;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import com.example.condor.data_objects.AuthData;
import com.example.condor.data_objects.UserData;
import com.example.condor.services.UserService;

@RestController
@RequestMapping("/api/v1/users")
public class UserController {

    @Autowired
    private UserService userServices;

    /**
     * This service is used to get a user by the id.
     *
     * @param id
     * @return user information
     */
    @GetMapping("/by_id/{idUser}")
    public Optional<UserData> getUserById(@PathVariable("idUser") Integer id) {
        return userServices.getUserById(id);
    }

    /**
     * This service is used to authenticate an user in the application.
     *
     * @param authData
     * @return An object with user data if it is authenticated.
     */
    @PostMapping("/auth")
    public Optional<UserData> authUser(@RequestBody AuthData authData) {
        return userServices.authUser(authData);
    }

    /**
     * This service is used to add a new user in the application.
     *
     * @param userData
     * @return An object with user data.
     */
    @PostMapping("/add_user")
    @ResponseStatus(HttpStatus.CREATED)
    public UserData createUser(@RequestBody UserData userData) {
        return userServices.addUser(userData);
    }

    /**
     * This service is used to update the password of a user.
     *
     * @param userData
     * @return A boolean value to indicate if the password was updated.
     */
    @PatchMapping("/update_password")
    @ResponseStatus(HttpStatus.CREATED)
    public Boolean updatePassword(@RequestBody UserData userData) {
        return userServices.updatePassword(userData);
    }

    /**
     * This service is used to delete a user by the id.
     *
     * @param id
     * @return A boolean value to indicate if the user was deleted.
     */
    @DeleteMapping("/delete_user/{idUser}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Boolean deleteUser(@PathVariable("idUser") Integer id) {
        return userServices.deleteUser(id);
    }
}

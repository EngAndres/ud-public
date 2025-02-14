/**
 * This is a class to handle web services
 * related to user functionalities.
 * 
 * Author: Carlos Andres Sierra <casierrav@udistrital.edu.co>
 */

package com.ud.machines.controllers;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import com.ud.machines.data_objects.AuthData;
import com.ud.machines.data_objects.UserData;
import com.ud.machines.services.UserServiceProxy;

@RestController
@RequestMapping("/api/v1/users")
public class UserController {

    @Autowired
    private UserServiceProxy userServices;

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

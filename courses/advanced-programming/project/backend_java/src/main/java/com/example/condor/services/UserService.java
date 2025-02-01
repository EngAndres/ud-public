/**
 * This file has a class to handle user functionalities.
 * 
 * Author: Carlos Andres Sierra <
 */
package com.example.condor.services;

import java.util.Optional;
import com.example.condor.data_objects.UserData;
import com.example.condor.data_objects.AuthData;
import com.example.condor.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * This class is used to manage the user's data.
 */
@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    /**
     * This method is used to get a user by the id.
     *
     * @param id
     * @return user information
     */
    public Optional<UserData> getUserById(Integer id) {
        if (id < 0) {
            return Optional.empty();
        }
        return userRepository.getUserById(id);
    }

    /**
     * This method is used to authenticate an user in the application.
     *
     * @param authData
     * @return An object with user data if it is authenticated.
     */
    public Optional<UserData> authUser(AuthData authData) {
        if (authData.password == null || authData.username == null) {
            return Optional.empty();
        }
        return userRepository.authUser(authData);
    }

    /**
     * This method is used to add a new user in the application.
     *
     * @param userData
     * @return An object with user data.
     */
    public UserData addUser(UserData userData) {
        if (userData.name == null || userData.username == null || userData.password == null || userData.language == null || userData.location == null || userData.age < 0) {
            return null;
        }
        return userRepository.addUser(userData);
    }
}

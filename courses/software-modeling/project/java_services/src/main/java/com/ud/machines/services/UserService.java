/**
 * This file has a class to handle user functionalities.
 * 
 * Author: Carlos Andres Sierra <casierrav@udistrital.edu.co>
 */

package com.ud.machines.services;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;


import com.ud.machines.data_objects.AuthData;
import com.ud.machines.data_objects.UserData;
import com.ud.machines.repositories.UserRepository;

/**
 * This class is used to manage the user's data.
 */
@Service("userService")
public class UserService implements InterfaceUserService {

    @Autowired
    private UserRepository userRepository;

    /**
     * This method is used to get a user by the id.
     *
     * @param id
     * @return user information
     */
    @Override
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
    @Override
    public Optional<UserData> authUser(AuthData authData) {
        if (authData.getPassword() == null || authData.getUsername() == null) {
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
    @Override
    public UserData addUser(UserData userData) {
        if (userData.name == null || userData.username == null || userData.password == null || userData.language == null || userData.location == null || userData.age < 0) {
            return null;
        }
        return userRepository.addUser(userData);
    }

    /**
     * This method is used to update the password of a user.
     *
     * @param userData
     * @return A boolean value to indicate if the password was updated.
     */
    @Override
    public Boolean updatePassword(UserData userData) {
        if (userData.id < 0 || userData.password == null) {
            return false;
        }
        return userRepository.updatePassword(userData);
    }

    /**
     * This method is used to delete a user by the id.
     *
     * @param id
     * @return A boolean value to indicate if the user was deleted.
     */
    @Override
    public Boolean deleteUser(Integer id) {
        if (id < 0) {
            return false;
        }
        return userRepository.deleteUser(id);
    }
}

/**
 * This file has a class to define a proxy to handle user services
 * adding a logging layer.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

package com.ud.machines.services;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

import com.ud.machines.data_objects.AuthData;
import com.ud.machines.data_objects.UserData;
import com.ud.machines.repositories.LogRepository;

@Component
public class UserServiceProxy implements InterfaceUserService {

    private final InterfaceUserService delegate;
    private final LogRepository logRepository;

    @Autowired
    public UserServiceProxy(
            @Qualifier("userService") InterfaceUserService delegate,
            LogRepository logRepository) {
        this.delegate = delegate;
        this.logRepository = logRepository;
    }

    @Override
    public Optional<UserData> getUserById(Integer id) {
        logRepository.logInteraction("getUserById called with id: " + id);
        return delegate.getUserById(id);
    }

    @Override
    public Optional<UserData> authUser(AuthData authData) {
        logRepository.logInteraction("authUser called with username: " + authData.getUsername());
        return delegate.authUser(authData);
    }

    @Override
    public UserData addUser(UserData userData) {
        logRepository.logInteraction("addUser called for user: " + userData.getName());
        return delegate.addUser(userData);
    }

    @Override
    public Boolean updatePassword(UserData userData) {
        logRepository.logInteraction("updatePassword called for user id: " + userData.getId());
        return delegate.updatePassword(userData);
    }

    @Override
    public Boolean deleteUser(Integer id) {
        logRepository.logInteraction("deleteUser called for user id: " + id);
        return delegate.deleteUser(id);
    }
}
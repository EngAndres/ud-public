/**
 * This file is the InterfaceUserService file.
 * 
 * Author: <cavirguezs@uditrital.edu.co>
 */

package com.ud.machines.services; 

import java.util.Optional;

import com.ud.machines.data_objects.AuthData;
import com.ud.machines.data_objects.UserData;

public interface InterfaceUserService {
    
    public Optional<UserData> getUserById(Integer id);
    
    public Optional<UserData> authUser(AuthData authData);
    
    public UserData addUser(UserData userData);
    
    public Boolean updatePassword(UserData userData);

    public Boolean deleteUser(Integer id);
}
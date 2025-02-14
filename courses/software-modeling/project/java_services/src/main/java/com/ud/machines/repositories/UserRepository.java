/**
 * This file has a class to handle user data.
 *
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co?
 */
package com.ud.machines.repositories;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import javax.annotation.PostConstruct;

import org.springframework.stereotype.Repository;

import com.ud.machines.data_objects.AuthData;
import com.ud.machines.data_objects.UserData;

@Repository
public class UserRepository {

    private List<UserData> users = new ArrayList<>();
    private final String filePath = "data/users.json";

    @PostConstruct
    public void init() {
        System.out.println("Loading users data...");
        this.users = JSONOperations.loadData(this.filePath, UserData.class);
    }

    /**
     * This method is used to get a user by the id.
     *
     * @param id
     * @return user information
     */
    public Optional<UserData> getUserById(int id) {
        for (UserData user : this.users) {
            if (user.id == id) {
                return Optional.of(user);
            }
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
        for (UserData user : this.users) {
            if (user.username.equals(authData.getUsername()) && user.password.equals(authData.getPassword())) {
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
        for (UserData user : this.users) {
            if (user.id > last_id) {
                last_id = user.id;
            }
        }

        userData.id = last_id + 1;
        this.users.add(userData);
        JSONOperations.saveData(this.filePath, this.users);

        return userData;
    }

    /**
     * This method is used to update the password of a user.
     *
     * @param userData
     * @return A boolean value to indicate if the password was updated.
     */
    public Boolean updatePassword(UserData userData) {
        Boolean result = false;
        for (int i = 0; i < this.users.size(); i++) {
            if (this.users.get(i).id == userData.id) {
                this.users.get(i).password = userData.password;
                JSONOperations.saveData(this.filePath, this.users);
                result = true;
                break;
            }
        }

        return result;
    }

    /**
     * This method is used to delete a user by the id.
     *
     * @param id
     * @return A boolean value to indicate if the user was deleted.
     */
    public Boolean deleteUser(int id) {
        Boolean result = false;
        for (int i = 0; i < this.users.size(); i++) {
            if (this.users.get(i).id == id) {
                this.users.remove(i);
                JSONOperations.saveData(this.filePath, this.users);
                result = true;
                break;
            }
        }

        return result;
    }
}

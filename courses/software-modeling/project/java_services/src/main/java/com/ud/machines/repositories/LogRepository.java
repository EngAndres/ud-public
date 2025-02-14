/**
 * This file has a class to define a repository to handle
 * log information.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

package com.ud.machines.repositories;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import org.springframework.stereotype.Repository;

@Repository
public class LogRepository {

    private final String logFilePath = "src/main/resources/data/log.txt";

    public void logInteraction(String message) {
        try {
            File logFile = new File(logFilePath);
            // Check if parent directories exist; if not, create them.
            File parentDir = logFile.getParentFile();
            if (!parentDir.exists()) {
                parentDir.mkdirs();
            }
            // FileWriter in append mode creates the file if it does not exist.
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(logFile, true))) {
                writer.write(message);
                writer.newLine();
            }
        } catch (IOException e) {
            System.err.println("Error writing to log file: " + e.getMessage());
        }
    }
}

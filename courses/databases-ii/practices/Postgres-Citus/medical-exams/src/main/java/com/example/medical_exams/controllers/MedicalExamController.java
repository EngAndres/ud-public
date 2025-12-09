package com.example.medical_exams.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.medical_exams.models.MedicalExam;
import com.example.medical_exams.services.MedicalExamService;

import jakarta.validation.Valid;
import java.util.Optional;

@RestController
@RequestMapping("/api/exams")
public class MedicalExamController {
    
    @Autowired
    private MedicalExamService service;

    @PostMapping("/create")
    public Optional<MedicalExam> createExam(@Valid @RequestBody MedicalExam medicalExam){
        return service.save(medicalExam);
    }

    @GetMapping("/get_all")
    public List<MedicalExam> getAllExams(){
        return service.findAll();
    }

    @GetMapping("/get_by_id/{id}")
    public Optional<MedicalExam> getExamById(@PathVariable Integer id){
        return service.findById(id);
    }

    @GetMapping("/get_by_patient/{patientId}")
    public List<MedicalExam> getExamsByPatient(@PathVariable Long patientId){
        return service.findByPatientId(patientId);
    }

}

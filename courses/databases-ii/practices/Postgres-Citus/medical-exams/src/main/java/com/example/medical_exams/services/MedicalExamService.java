package com.example.medical_exams.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.medical_exams.models.MedicalExam;
import com.example.medical_exams.repositories.MedicalExamRepository;
import java.util.List;
import java.util.Optional;

@Service
public class MedicalExamService {

    @Autowired
    private MedicalExamRepository repo;

    public Optional<MedicalExam> save(MedicalExam medicalExam){
        try{
            return (MedicalExam) repo.save(medicalExam);
        } catch(Exception e){
            return null;
        }
    }

    public List<MedicalExam> findByPatientId(Long patientId){
        return repo.findByPatientId(patientId);
    }

    public List<MedicalExam> findAll(){
        return (List<MedicalExam>) repo.findAll();
    }

    public Optional<MedicalExam> findById(Integer id){
        return (Optional<MedicalExam>) repo.findById(id);
    }

    public void delete(Integer examId){
        repo.deleteById(examId);
    }
}

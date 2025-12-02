package com.example.medical_exams.repositories;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;
import com.example.medical_exams.models.MedicalExam;
import java.util.List;

@Repository
public interface MedicalExamRepository extends CrudRepository{
    
    /*
    SELECT * 
    FROM medical_exam
    WHERE patientId = 'patientId_parameter';
     */
    List<MedicalExam> findByPatientId(Long patientId);

    @Query("SELECT examType AS type, COUNT(type) AS count FROM medical_exam GROUP BY examType;")
    List<Object[]> countByExamType();
}

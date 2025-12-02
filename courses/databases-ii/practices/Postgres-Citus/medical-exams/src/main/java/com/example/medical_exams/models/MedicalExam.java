package com.example.medical_exams.models;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "medical_exam")
public class MedicalExam {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer examId;

    @Column(nullable = false)
    private Long patientId;

    @Column(nullable = false)
    private String examType;
    
    @Column
    private String result;

    @Column(nullable = false)
    private Instant createdAt;


    public MedicalExam(Long patientId, String examType, String result){
        this.patientId = patientId;
        this.examType = examType;
        this.result = result;
        this.createdAt = Instant.now();
    }

    public Integer getExamId() {
        return examId;
    }

    public Long getPatientId() {
        return patientId;
    }

    public void setPatientId(Long patientId) {
        this.patientId = patientId;
    }

    public String getExamType() {
        return examType;
    }

    public void setExamType(String examType) {
        this.examType = examType;
    }

    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }
}

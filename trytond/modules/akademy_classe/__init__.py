# This file is part of SAGE Education.   The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from . import classe
from . import company
from . import configuration
from . import report

def register():
    Pool.register(   
        company.Employee,
        company.Student,
        classe.Classes, 
        classe.ClasseTimeRule,
        classe.ClasseStudent,
        classe.ClasseStudentDiscipline, 
        classe.ClasseTeacher, 
        classe.ClasseTeacherDiscipline,
        classe.ClasseTeacherLesson,
        classe.ClasseStudentPresence,
        classe.ClasseTeacherPresence,
        configuration.LectiveYear,
        configuration.Quarter,
        configuration.Area,
        configuration.Course,
        configuration.Classe,
        configuration.CourseClasse,
        configuration.AcademicLevel,
        configuration.TimeCourse, 
        configuration.MetricAvaliation,
        configuration.Avaliation,
        configuration.AvaliationType,
        configuration.Discipline,
        configuration.ClasseRoom,
        configuration.StudyPlan, 
        configuration.StudyPlanDiscipline,
        configuration.DisciplinePrecedents,
        configuration.StudyPlanAvaliation, 
        configuration.DisciplineState,
        configuration.DisciplineModality,
        configuration.MatriculationState,
        configuration.MatriculationType,
        configuration.ClasseTimeType, 
        configuration.ClasseLessonType,  
        
        module='akademy_classe', type_='model'
    )

    Pool.register(
        report.AcademicLevelReport,
        report.StudyplanReport,
        report.ClassesReport,
        report.ClassesDisciplineLessonsReport,
        report.MatriculationReport,
        report.MatriculationStateReport,
        report.MatriculationTeacherReport, 
        report.ClasseStudentTimeRuleReport,
        report.ClasseTeacherTimeRuleReport,

        module='akademy_classe', type_='report'               
    )


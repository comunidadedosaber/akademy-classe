# This file is part of SAGE Education.   The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from trytond.report import Report
from datetime import date



class AcademicLevelReport(Report):
	__name__ = 'akademy_report.academic.level.report'

	@classmethod
	def get_context(cls, records, header, data):
		AcademicLevel = Pool().get('akademy_configuration.academic.level')

		context = super().get_context(records, header, data)
		academic_level = AcademicLevel.browse(data['ids'])

		context['academic_level'] = academic_level
		context['create_date'] = date.today()
		return context


class StudyplanReport(Report):
	__name__ = 'akademy_report.studyplan.report'

	@classmethod
	def get_context(cls, records, header, data):
		Studyplan = Pool().get('akademy_configuration.studyplan')

		context = super().get_context(records, header, data)
		studyplan = Studyplan.browse(data['ids'])
        
		context['studyplans'] = studyplan
		context['create_date'] = date.today()
		return context


class ClassesReport(Report):
	__name__ = 'akademy_report.classes.report'

	@classmethod
	def get_context(cls, records, header, data):
		Classes = Pool().get('akademy_classe.classes')

		context = super().get_context(records, header, data)
		classes = Classes.browse(data['ids'])

		context['classes'] = classes
		context['create_date'] = date.today()
		return context


class ClasseStudentTimeRuleReport(Report):
	__name__ = 'akademy_report.classe.student.timerule.report'

	@classmethod
	def get_context(cls, records, header, data):
		ClasseStudent = Pool().get('akademy_classe.classe.student')
		ClasseTimeRule = Pool().get('akademy_classe.classe.timerule')

		context = super().get_context(records, header, data)
		classe_student = ClasseStudent.browse(data['ids'])

		classe_timerule = ClasseTimeRule.search([
			('classes', '=', classe_student[0].classes)], 
			order=[('lesson_time.name', 'ASC')
		  	])
		timerule_time = []
		classe_student_timerules = []
		classe_student_timerule = []
		mon = None
		tue = None
		wed = None
		thu = None
		fri = None
		sat = None
		lesson_time = None
		start_lesson = None
		end_lesson = None

		for classe_student_discipline in classe_student[0].classe_student_discipline:
			for timerule in classe_timerule:		
				print(timerule.lesson_time.name, classe_student_discipline.studyplan_discipline.discipline.name)	
				if classe_student_discipline.studyplan_discipline == timerule.mon:
					mon = timerule.mon.discipline.name					
					lesson_time = timerule.lesson_time.name
					start_lesson = timerule.start_lesson
					end_lesson = timerule.end_lesson

				if classe_student_discipline.studyplan_discipline == timerule.tue:
					tue = timerule.tue.discipline.name					
					lesson_time = timerule.lesson_time.name
					start_lesson = timerule.start_lesson
					end_lesson = timerule.end_lesson

				if classe_student_discipline.studyplan_discipline == timerule.wed:
					wed = timerule.wed.discipline.name					
					lesson_time = timerule.lesson_time.name
					start_lesson = timerule.start_lesson
					end_lesson = timerule.end_lesson

				if classe_student_discipline.studyplan_discipline == timerule.thu:
					thu = timerule.thu.discipline.name					
					lesson_time = timerule.lesson_time.name
					start_lesson = timerule.start_lesson
					end_lesson = timerule.end_lesson

				if classe_student_discipline.studyplan_discipline == timerule.fri:
					fri = timerule.fri.discipline.name					
					lesson_time = timerule.lesson_time.name
					start_lesson = timerule.start_lesson
					end_lesson = timerule.end_lesson

				if classe_student_discipline.studyplan_discipline == timerule.sat:
					sat = timerule.sat.discipline.name					
					lesson_time = timerule.lesson_time.name
					start_lesson = timerule.start_lesson
					end_lesson = timerule.end_lesson
				
				if start_lesson:
					classe_student_timerule.append([
						timerule.classes, lesson_time, start_lesson, end_lesson, mon, tue, wed, thu, fri, sat
						])
				lesson_time = None
				start_lesson = None
				end_lesson = None
				mon = None
				tue = None
				wed = None
				thu = None
				fri = None
				sat = None

		
		for timerule in classe_timerule:
			classes = None	
			for copy_timerule in classe_student_timerule:
				if copy_timerule[1] ==  timerule.lesson_time.name:

					if copy_timerule[0]:
						classes = copy_timerule[0]
					if copy_timerule[1]:
						lesson_time = copy_timerule[1]
					if copy_timerule[2]:
						start_lesson = copy_timerule[2]
					if copy_timerule[3]:
						end_lesson = copy_timerule[3] 
					if copy_timerule[4]:
						mon = copy_timerule[4] 
					if copy_timerule[5]:
						tue = copy_timerule[5] 
					if copy_timerule[6]:
						wed = copy_timerule[6]
					if copy_timerule[7]:
						thu = copy_timerule[7]
					if copy_timerule[8]:
						fri = copy_timerule[8]
					if copy_timerule[9]:
						sat = copy_timerule[9]

			classe_student_timerules.append([
				classes,
				lesson_time,
				start_lesson,
				end_lesson,
				mon,
				tue,
				wed,
				thu,
				fri,
				sat,
				])	
			lesson_time = None
			start_lesson = None
			end_lesson = None
			mon = None
			tue = None
			wed = None
			thu = None
			fri = None
			sat = None		
		
		context['classe_student_timerules'] = classe_student_timerules #.append(classe_student_timerule)
		context['create_date'] = date.today()
		return context


class ClasseTeacherTimeRuleReport(Report):
	__name__ = 'akademy_report.classe.teacher.timerule.report'

	@classmethod
	def get_context(cls, records, header, data):
		ClasseTeacher= Pool().get('akademy_classe.classe.teacher')
		ClasseTimeRule = Pool().get('akademy_classe.classe.timerule')

		context = super().get_context(records, header, data)
		classe_teacher = ClasseTeacher.browse(data['ids'])

		classe_timerule = ClasseTimeRule.search([
			('classes', '=', classe_teacher[0].classes)], 
			order=[('lesson_time.name', 'ASC')
		  	])
		
		classe_teacher_timerules = []
		classe_teacher_timerule = []
		mon = None
		tue = None
		wed = None
		thu = None
		fri = None
		sat = None
		lesson_time = None
		start_lesson = None
		end_lesson = None

		for classe_teacher_discipline in classe_teacher[0].classe_teacher_discipline:
			for timerule in classe_timerule:		
				
				if classe_teacher_discipline.studyplan_discipline == timerule.mon:
					mon = timerule.mon.discipline.name					
					lesson_time = timerule.lesson_time.name
					start_lesson = timerule.start_lesson
					end_lesson = timerule.end_lesson

				if classe_teacher_discipline.studyplan_discipline == timerule.tue:
					tue = timerule.tue.discipline.name					
					lesson_time = timerule.lesson_time.name
					start_lesson = timerule.start_lesson
					end_lesson = timerule.end_lesson

				if classe_teacher_discipline.studyplan_discipline == timerule.wed:
					wed = timerule.wed.discipline.name					
					lesson_time = timerule.lesson_time.name
					start_lesson = timerule.start_lesson
					end_lesson = timerule.end_lesson

				if classe_teacher_discipline.studyplan_discipline == timerule.thu:
					thu = timerule.thu.discipline.name					
					lesson_time = timerule.lesson_time.name
					start_lesson = timerule.start_lesson
					end_lesson = timerule.end_lesson

				if classe_teacher_discipline.studyplan_discipline == timerule.fri:
					fri = timerule.fri.discipline.name					
					lesson_time = timerule.lesson_time.name
					start_lesson = timerule.start_lesson
					end_lesson = timerule.end_lesson

				if classe_teacher_discipline.studyplan_discipline == timerule.sat:
					sat = timerule.sat.discipline.name					
					lesson_time = timerule.lesson_time.name
					start_lesson = timerule.start_lesson
					end_lesson = timerule.end_lesson
				
				if start_lesson:
					classe_teacher_timerule.append([
						timerule.classes, lesson_time, start_lesson, end_lesson, mon, tue, wed, thu, fri, sat
						])
				lesson_time = None
				start_lesson = None
				end_lesson = None
				mon = None
				tue = None
				wed = None
				thu = None
				fri = None
				sat = None

		
		for timerule in classe_timerule:
			classes = None	
			for copy_timerule in classe_teacher_timerule:
				if copy_timerule[1] ==  timerule.lesson_time.name:

					if copy_timerule[0]:
						classes = copy_timerule[0]
					if copy_timerule[1]:
						lesson_time = copy_timerule[1]
					if copy_timerule[2]:
						start_lesson = copy_timerule[2]
					if copy_timerule[3]:
						end_lesson = copy_timerule[3] 
					if copy_timerule[4]:
						mon = copy_timerule[4] 
					if copy_timerule[5]:
						tue = copy_timerule[5] 
					if copy_timerule[6]:
						wed = copy_timerule[6]
					if copy_timerule[7]:
						thu = copy_timerule[7]
					if copy_timerule[8]:
						fri = copy_timerule[8]
					if copy_timerule[9]:
						sat = copy_timerule[9]

			classe_teacher_timerules.append([
				classes,
				lesson_time,
				start_lesson,
				end_lesson,
				mon,
				tue,
				wed,
				thu,
				fri,
				sat,
				])	
			lesson_time = None
			start_lesson = None
			end_lesson = None
			mon = None
			tue = None
			wed = None
			thu = None
			fri = None
			sat = None		
		
		context['classe_teacher_timerules'] = classe_teacher_timerules #.append(classe_student_timerule)
		context['create_date'] = date.today()
		return context


class MatriculationReport(Report):
	__name__ = 'akademy_report.matriculation.report'

	@classmethod
	def get_context(cls, records, header, data):
		Matriculation = Pool().get('akademy_classe.classe.student')

		context = super().get_context(records, header, data)
		matriculation = Matriculation.browse(data['ids'])

		context['matriculation'] = matriculation
		context['create_date'] = date.today()
		return context


class MatriculationStateReport(Report):
	__name__ = 'akademy_report.matriculation.state.report'

	@classmethod
	def get_context(cls, records, header, data):
		Matriculation = Pool().get('akademy_classe.classe.student')

		context = super().get_context(records, header, data)
		matriculation = Matriculation.browse(data['ids'])		

		context['matriculation'] = matriculation
		context['create_date'] = date.today()
		return context


class MatriculationTeacherReport(Report):
	__name__ = 'akademy_report.matriculation.teacher.report'

	@classmethod
	def get_context(cls, records, header, data):
		Matriculation = Pool().get('akademy_classe.classe.teacher')

		context = super().get_context(records, header, data)
		matriculations = Matriculation.browse(data['ids'])		

		context['matriculation'] = matriculations
		context['create_date'] = date.today()
		return context


class ClassesDisciplineLessonsReport(Report):
	__name__ = 'akademy_report.classes.discipline.lessons.report'

	@classmethod
	def get_context(cls, records, header, data):
		TeacherDisciplineLessons = Pool().get('akademy_classe.classe.teacher.lesson')

		context = super().get_context(records, header, data)
		discipline_lessons = TeacherDisciplineLessons.browse(data['ids'])

		context['discipline_lessons'] = discipline_lessons
		context['create_date'] = date.today()
		return context



# This file is part of SAGE Education.   The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields, Unique, Check
from trytond.pyson import Eval
from trytond.pool import Pool
from trytond.exceptions import UserError
from datetime import date


_PRESENCES = [
    ('presente', 'Presente'),
	('ausente', 'Ausente'),
]


class Classes(ModelSQL, ModelView):
	'Classes'
	__name__ = 'akademy_classe.classes'

	code = fields.Char('Código', size=20,
		help="Código da turma.")
	name = fields.Char('Nome', required=True,
		help="Nome da turma.")	
	max_student = fields.Integer('Discentes', 
		help="Limite máximo de discentes por adicionar na turma.")
	max_teacher = fields.Integer('Docentes', 
		help="Limite máximo de docentes por adicionar na turma.")
	modality = fields.Many2One(
        'akademy_configuration.discipline.modality', 'Modalidade', 
        required=True, ondelete="RESTRICT",
		help="Escolha a modalidade de frequência.")
	classe = fields.Many2One(
		'akademy_configuration.classe', 'Classe', 
		required=True, ondelete="RESTRICT",
		help="Nome da classe.")
	time_course = fields.Many2One(
		'akademy_configuration.time.course', 'Período', 
		required=True, ondelete="RESTRICT")
	lective_year = fields.Many2One(
		'akademy_configuration.lective.year', 'Ano letivo', 
		required=True, ondelete="RESTRICT",
		help="Nome do ano letivo.")
	studyplan = fields.Many2One('akademy_configuration.studyplan', 
		'Plano de estudo', required=True, ondelete="RESTRICT") 	
	classe_timerule = fields.One2Many('akademy_classe.classe.timerule', 
		'classes', 'Horário')
	classe_student = fields.One2Many('akademy_classe.classe.student', 
		'classes', 'Lista de discentes')
	classe_teacher = fields.One2Many('akademy_classe.classe.teacher', 
		'classes', 'Lista de docentes')
	classe_teacher_lesson = fields.One2Many('akademy_classe.classe.teacher.lesson', 
		'classes', 'Plano de aula')
	
	@classmethod
	def __setup__(cls):
		super(Classes, cls).__setup__()
		table = cls.__table__()
		cls._sql_constraints = [
			('key', Unique(table, table.code, table.name, table.classe, table.lective_year),
			u'Não foi possível cadastrar a nova turma, por favor verificar se já existe uma turma com este nome para este ano letivo.'),
			('student', Check(table, table.max_student > 0),
			u'Não foi possível adicionar o discente a turma, por favor verifica o limite de vagas existente na turma.'),
			('teacher', Check(table, table.max_teacher > 0),
			u'Não foi possível adicionar o docente na turma, por favor verifica o limite de vagas existente na turma.')
		]
	
	@classmethod
	def default_max_student(cls):
		return 1

	@classmethod
	def default_max_teacher(cls):
		return 1


class ClasseStudent(ModelSQL, ModelView):
	'Classe Student'
	__name__ = 'akademy_classe.classe.student'

	description = fields.Text('Descrição')
	state = fields.Many2One(
		'akademy_configuration.matriculation.state', 'Estado', 
		required=True, help="Escolha o estado de matrícula.")
	type = fields.Many2One(
		'akademy_configuration.matriculation.type', 'Tipo', 
		required=True, help="Escolha o tipo de matrícula.")
	student = fields.Many2One('company.student', 'Discente', 
		required=True, ondelete="RESTRICT")
	classes = fields.Many2One('akademy_classe.classes', 'Turma', 
		required=True, ondelete="RESTRICT")
	classe_student_discipline = fields.One2Many(
		'akademy_classe.classe.student.discipline', 'classe_student', 
		'Discente disciplina')
	classe_student_presence= fields.One2Many(
		'akademy_classe.classe.student.presence', 'classe_student', 
		'Presenças')

	@classmethod
	def __setup__(cls):
		super(ClasseStudent, cls).__setup__()
		table = cls.__table__()
		cls._sql_constraints = [
			('key', Unique(table, table.student, table.classes), 
			u'Não foi possivél cadastrar o novo discente, por favor verificar se o discente já está matriculado nesta turma.')
		]
		cls._order = [('student.party.name', 'ASC')]

	def get_rec_name(self, name):
		t1 = '%s' % \
			(self.student.rec_name)
		return t1
	
	@classmethod
	def save_student_matriculation(cls, matriculation_state, matriculation_type, student, classes): 
		ClasseStudent = Pool().get('akademy_classe.classe.student')  
				
		max_student = classes.max_student + 1
		if classes.max_student < max_student: 								
			student_matriculation = ClasseStudent(
				state = matriculation_state,
				type = matriculation_type,
				student = student,
				classes = classes,
			)
			student_matriculation.save()	

		else:
			raise UserError("Já excedeu o limite de vagas disponíveis na turma.")

		return student_matriculation


class ClasseStudentDiscipline(ModelSQL, ModelView):
	'Classe Student Discipline'
	__name__ = 'akademy_classe.classe.student.discipline'

	code = fields.Char('Código', size=25)
	state = fields.Many2One(
		'akademy_configuration.matriculation.state', 'Estado', 
		required=True, help="Escolha o estado de matrícula.")
	modality = fields.Many2One(
		'akademy_configuration.discipline.modality',  'Modalidade', 
		required=True, help="Escolha a modalidade de frequência.")	
	classe_student = fields.Many2One('akademy_classe.classe.student', 
		'Discente', required=True, ondelete="RESTRICT")
	classes = fields.Function(
		fields.Many2One(
			'akademy_classe.classes', 'Turma', 
		), 'on_change_with_classes')
	studyplan_discipline = fields.Many2One(
		'akademy_configuration.studyplan.discipline', 'Disciplina', 
		domain=[('studyplan.classes', '=', Eval('classes', -1))],
		depends=['classes'], required=True, ondelete="RESTRICT")

	@classmethod
	def __setup__(cls):
		super(ClasseStudentDiscipline, cls).__setup__()
		table = cls.__table__()
		cls._sql_constraints = [
			('key', Unique(table, table.classe_student, table.studyplan_discipline),
			u'Não foi possivél associar o discente a disciplina, por favor verificar se o mesmo já está a frequentar esta disciplina na turma.')
		]
		cls._order = [('classe_student.student.party.name', 'ASC')]

	def get_rec_name(self, name):
		t1 = '%s - %s' % \
			(self.studyplan_discipline.rec_name, self.classe_student.rec_name)
		return t1

	@fields.depends('classe_student')
	def on_change_with_classes(self, name=None):
		if self.classe_student.classes:
			return self.classe_student.classes
		
		raise UserError("por favor verificar se o discente esta associado a uma turma.")

	@classmethod
	def save_student_discipline(cls, StudentClasse, StudyplanDiscipline, state, modality):		
		matriculaton = ClasseStudentDiscipline(
			classe_student = StudentClasse,
			studyplan_discipline = StudyplanDiscipline,
			state = state,
			modality = modality,
		)
		matriculaton.save()


class ClasseTeacher(ModelSQL, ModelView):
	'Classe Teacher'
	__name__ = 'akademy_classe.classe.teacher'
		
	state = fields.Many2One('akademy_configuration.matriculation.state', 
		'Estado', required=True, help="Escolha o estado de matrícula.")
	description = fields.Text('Descrição')
	employee = fields.Many2One('company.employee', 'Funcionário', 
		required=True, ondelete="RESTRICT",
		domain=[('teacher', '=', True)])
	classes = fields.Many2One('akademy_classe.classes', 'Turma', 
		required=True, ondelete="RESTRICT")
	classe_teacher_discipline = fields.One2Many('akademy_classe.classe.teacher.discipline', 
		'classe_teacher', 'Disciplina')
	classe_teacher_lesson = fields.One2Many('akademy_classe.classe.teacher.lesson', 
		'classe_teacher', 'Plano de aula')
	classe_teacher_presence= fields.One2Many(
		'akademy_classe.classe.teacher.presence', 'classe_teacher', 
		'Presenças')

	@classmethod
	def __setup__(cls):
		super(ClasseTeacher, cls).__setup__()
		table = cls.__table__()
		cls._sql_constraints += [
			('key', Unique(table, table.employee, table.classes), 
			u'Não foi possivél matricular o docente, por favor verificar se o docente já existe na turma.')
		]
		cls._order = [('employee.party.name', 'ASC')]

	def get_rec_name(self, name):
		t1 = '%s' % \
			(self.employee.rec_name)
		return t1


class ClasseTeacherDiscipline(ModelSQL, ModelView):
	'Classe Teacher Discipline'
	__name__ = 'akademy_classe.classe.teacher.discipline'
			
	state = fields.Many2One('akademy_configuration.matriculation.state', 
		'Estado', required=True, help="Escolha o estado de matrícula.")
	modality = fields.Many2One('akademy_configuration.discipline.modality', 
		'Modalidade', required=True, help="Escolha a modalidade de frequência.")	
	classe_teacher = fields.Many2One('akademy_classe.classe.teacher', 'Docente', 
		required=True, ondelete="RESTRICT")
	classes = fields.Function(
		fields.Many2One(
			'akademy_classe.classes', 'Turma', 
		), 'on_change_with_classes')
	studyplan_discipline = fields.Many2One('akademy_configuration.studyplan.discipline', 'Disciplina', 
		domain=[('studyplan.classes', '=', Eval('classes', -1))],
		depends=['classes'], required=True, ondelete="RESTRICT"
	)

	@classmethod
	def __setup__(cls):
		super(ClasseTeacherDiscipline, cls).__setup__()
		table = cls.__table__()
		cls._sql_constraints = [
			('key', Unique(table, table.classe_teacher, table.studyplan_discipline),
			u'Não foi possivél associar o docente a disciplina, por favor verificar se o mesmo já está a lecionar esta disciplina na turma.')
		]
		cls._order = [('studyplan_discipline.discipline', 'ASC')]

	def get_rec_name(self, name):
		t1 = '%s - %s' % \
			(self.studyplan_discipline.rec_name, self.classe_teacher.rec_name)
		return t1

	@fields.depends('classe_teacher')
	def on_change_with_classes(self, name=None):
		if self.classe_teacher.classes:
			return self.classe_teacher.classes
		
		raise UserError("por favor verificar se o docente esta associado a uma turma.")


class ClasseTeacherLesson(ModelSQL, ModelView):
	'Classes Teacher Lesson'
	__name__ = 'akademy_classe.classe.teacher.lesson'		

	lesson_number = fields.Char('Lição nº', size=25, required=True,
		help="Insira o número da aula ou alas.\nExemplo: 1 ou 1 e 2")	
	objective = fields.Text('Objectivos')
	unidate = fields.Char('Unidade', required=True)
	summary = fields.Text('Sumário')
	lesson_date = fields.Date('Data', required=True)
	lesson_type = fields.Many2One('akademy_configuration.classe.lesson.type', 
		'Tipo de aula', required=True, ondelete="RESTRICT", 
		help="Escolha o tipo de aula.")	
	classes = fields.Many2One('akademy_classe.classes', 'Turma',
		domain=[('classe_teacher', '=', Eval('classe_teacher', -1))],
		required=True, depends=['classe_teacher'], ondelete="RESTRICT")
	classe_timerule = fields.Many2One('akademy_classe.classe.timerule', 'Horário',  
		domain=[('classes', '=', Eval('classes', -1))],
		required=True, depends=['classes'], ondelete="RESTRICT")		
	studyplan_discipline = fields.Many2One('akademy_configuration.studyplan.discipline', 
		'Disciplina', required=True, depends=['classe_teacher'],
		domain=[
			('classe_teacher_discipline.classe_teacher', '=', Eval('classe_teacher', -1))
			], ondelete="RESTRICT")
	classe_teacher = fields.Many2One(
		'akademy_classe.classe.teacher', 'Docente',
		domain=[('classes', '=', Eval('classes', -1))],
		depends=['classes'], required=True, ondelete="RESTRICT")
	
	@classmethod
	def default_lesson_date(cls):
		return date.today()


class ClasseTimeRule(ModelSQL, ModelView):
	'Classe TimeRule'
	__name__ = 'akademy_classe.classe.timerule'
	
	lesson_time = fields.Many2One('akademy_configuration.classe.time.type', 
		'Tempo', required=True, ondelete="RESTRICT", help="Escolha o tempo letivo.")	
	start_lesson = fields.Time('Entrada', format='%H:%M', required=True)
	end_lesson = fields.Time('Saída', format='%H:%M', required=True)		
	classes = fields.Many2One('akademy_classe.classes', 'Turma', 
		required=True, ondelete="RESTRICT")	
	mon = fields.Many2One(
		'akademy_configuration.studyplan.discipline', 'Segunda-feira',
		domain=[('studyplan.classes', '=', Eval('classes', -1))], depends=['classes'],
		help="Escolha a disciplina a ser lecionada na Segunda-feira.")
	tue = fields.Many2One(
		'akademy_configuration.studyplan.discipline', 'Terça-feira', 
		domain=[('studyplan.classes', '=', Eval('classes', -1))], depends=['classes'],
		help="Escolha a disciplina a ser lecionada na Terça-feira.")
	wed = fields.Many2One(
		'akademy_configuration.studyplan.discipline', 'Quarta-feira', 
		domain=[('studyplan.classes', '=', Eval('classes', -1))], depends=['classes'],
		help="Escolha a disciplina a ser lecionada na Quarta-feira.")
	thu = fields.Many2One(
		'akademy_configuration.studyplan.discipline', 'Quinta-feira',
		domain=[('studyplan.classes', '=', Eval('classes', -1))], depends=['classes'],
		help="Escolha a disciplina a ser lecionada na Quinta-feira.")
	fri = fields.Many2One(
		'akademy_configuration.studyplan.discipline', 'Sexta-feira',
		domain=[('studyplan.classes', '=', Eval('classes', -1))], depends=['classes'],
		help="Escolha a disciplina a ser lecionada na Sexta-feira.")
	sat = fields.Many2One(
		'akademy_configuration.studyplan.discipline', 'Sábado',
		domain=[('studyplan.classes', '=', Eval('classes', -1))], depends=['classes'],
		help="Escolha a disciplina a ser lecionada no Sábado.")
	mon_room = fields.Many2One('akademy_configuration.classe.room', 'Sala', 
		help="Escolha a sala de aula em que a disciplina vai ser lecionada na Segunda-feira.")
	tue_room = fields.Many2One('akademy_configuration.classe.room', 'Sala', 
		help="Escolha a sala de aula em que a disciplina vai ser lecionada na Terça-feira.")
	wed_room = fields.Many2One('akademy_configuration.classe.room', 'Sala', 
		help="Escolha a sala de aula em que a disciplina vai ser lecionada na Quarta-feira.")
	thu_room = fields.Many2One('akademy_configuration.classe.room', 'Sala', 
		help="Escolha a sala de aula em que a disciplina vai ser lecionada na Quinta-feira.")
	fri_room = fields.Many2One('akademy_configuration.classe.room', 'Sala', 
		help="Escolha a sala de aula em que a disciplina vai ser lecionada na Sexta-feira.")
	sat_room = fields.Many2One('akademy_configuration.classe.room', 'Sala', 
		help="Escolha a sala de aula em que a disciplina vai ser lecionada no Sábado.")

	@classmethod
	def __setup__(cls):
		super(ClasseTimeRule, cls).__setup__()
		table = cls.__table__()
		cls._sql_constraints += [
			('key', Unique(table, table.classes, table.lesson_time, table.start_lesson, table.end_lesson),
			u'Não foi possivél definir o tempo letivo para a turma, por favor verificar se o tempo letivo já existe para este horário.'),
			('time', Check(table, table.start_lesson < table.end_lesson),
			u'Não foi possivél definir o tempo letivo para a turma, por favor verifica a hora de entrada e saída.'),
		]
		cls._order = [('lesson_time.name', 'ASC')]

	def get_rec_name(self, name):
		t1 = '%s' % \
			(self.lesson_time.rec_name)
		return str(t1)


class ClasseTeacherPresence(ModelSQL, ModelView):
	'Classe Teacher Presence'
	__name__ = 'akademy_classe.classe.teacher.presence'

	presence = fields.Selection(_PRESENCES, 'Presença', required=True)
	classe_teacher = fields.Many2One('akademy_classe.classe.teacher', 
		'Docente', required=True)
	classe_timerule = fields.Many2One('akademy_classe.classe.timerule', 
		'Horário', required=True)
	classe_teacher_discipline = fields.Many2One('akademy_classe.classe.teacher.discipline', 
		'Disciplina', required=True, ondelete="RESTRICT", depends=['classe_teacher'], 
		domain=[('classe_teacher', '=', Eval('classe_teacher', -1))])


class ClasseStudentPresence(ModelSQL, ModelView):
	'Classe Student Presence'
	__name__ = 'akademy_classe.classe.student.presence'

	presence = fields.Selection(_PRESENCES, 'Presença', required=True)
	classe_student = fields.Many2One('akademy_classe.classe.student', 'Discente',)
	classe_timerule = fields.Many2One('akademy_classe.classe.timerule', 'Horário', 
		required=True)
	classe_student_discipline = fields.Many2One('akademy_classe.classe.student.discipline', 
		'Disciplina', required=True, ondelete="RESTRICT", depends=['classe_student'], 
		domain=[('classe_student', '=', Eval('classe_student', -1))])

	@classmethod
	def create(cls, vlist):
		state_student = ['Aguardando', 'Suspenso(a)', 'Anulada', 'Transfêrido(a)', 'Reprovado(a)', 'Aprovado(a)', 'Espera']
		vlist = [x.copy() for x in vlist]

		for values in vlist:
			ClasseStudentDiscipline = Pool().get('akademy_classe.classe.student.discipline')
			ClasseStudentPresence = Pool().get('akademy_classe.classe.student.presence')
			classe_student_discipline = ClasseStudentDiscipline(values['classe_student_discipline'])

			if classe_student_discipline.state.name in state_student:
				raise UserError("Não foi possível aplicar a falta ao discente nesta disciplina, por favor verificar se a matrícula se encontra em um deste estados.\n"+
					"Aguardando, Suspenso(a), Anulada, Transfêrido(a), Reprovado(a), Aprovado(a), Espera")

			studyplan_discipline_flaut = classe_student_discipline.studyplan_discipline.flaut

			classe_student_presence = ClasseStudentPresence.search([
				('classe_student', '=', values['classe_student']),
				('classe_student_discipline', '=', values['classe_student_discipline']),
				('presence', '=', 'absent')
				])

			if values['presence'] == "absent":
				#Total de faltas + nova falta
				student_discipline_flaut = len(classe_student_presence) + 1
			else:
				student_discipline_flaut = len(classe_student_presence)

			if studyplan_discipline_flaut < student_discipline_flaut:
				raise UserError("Não foi possível aplicar a falta ao discente nesta disciplina, porque já atingiu o limite de faltas establecido.")
				
			if studyplan_discipline_flaut == student_discipline_flaut:
				MatriculationState = Pool().get('akademy_configuration.matriculation.state')
				# Discente está reprovado(a) na discplina	
				matriculation_state = MatriculationState.search([
					('name', '=', "Reprovado(a)")
					], limit=1)

				classe_student_discipline.state = matriculation_state[0]
				classe_student_discipline.save()				
				
			return super(ClasseStudentPresence, cls).create(vlist)
			


// glsl.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include <glew.h>
#include <stdio.h>
#include <stdlib.h>
#include <glaux.h>
#include <glut.h>
#pragma comment (lib, "glew32.lib") 
#pragma comment (lib, "GLAUX.lib") 
GLfloat LightAmbient0[]= {0.8, 0.8, 0.8, 1.0f };
GLfloat LightDiffuse0[]= {1.0f, 1.0f, 1.0f, 1.0f };
GLfloat LightSpecular0[]={1.0f, 1.0f, 1.0f, 1.0f};
GLfloat LightPosition0[]= {3.0f, 3.0f, 3.0f, 0.0f };
GLfloat MaterialAmbient[] = {0.3, 0.3, 0.3, 1.0f};
GLfloat MaterialDiffuse[] = {0.7, 0.7, 0.7, 1.0f};
GLfloat MaterialSpecular[] ={0.3, 0.3, 0.3, 1.0f};
GLfloat MaterialSe = 64.0f;
GLUquadricObj *quadratic;
float a = 0.0f;
void printShaderInfoLog(GLuint obj);
void printProgramInfoLog(GLuint obj);
AUX_RGBImageRec *TextureImage[1];
GLuint texture;
void renderScene(void) {
	glClear(GL_COLOR_BUFFER_BIT |
		GL_DEPTH_BUFFER_BIT);
	glLoadIdentity();
	gluLookAt(0.0,0.0,5.0, 0.0,0.0,-1.0, 0.0f,1.0f,0.0f);
	a += 0.05f;
	if(a > 360)
		a -= 360.0f;
	glRotatef(a, 0, 1, 0);
	glRotatef(-90, 1, 0, 0);
	gluSphere(quadratic, 1, 32, 16);
	glutPostRedisplay();
	glutSwapBuffers();
}
void init()
{
	glEnable(GL_DEPTH_TEST);
	glClearColor(0.0,0.0,0.0,0.0);
	glEnable(GL_CULL_FACE);
	glEnable(GL_LIGHTING);
	glLightfv(GL_LIGHT0, GL_AMBIENT, LightAmbient0);
	glLightfv(GL_LIGHT0, GL_DIFFUSE, LightDiffuse0);
	glLightfv(GL_LIGHT0,GL_SPECULAR, LightSpecular0);
	glLightfv(GL_LIGHT0, GL_POSITION, LightPosition0);
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, MaterialAmbient);
	glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, MaterialDiffuse);
	glMaterialfv(GL_FRONT_AND_BACK,GL_SPECULAR, MaterialSpecular);
	glMaterialf(GL_FRONT_AND_BACK,GL_SHININESS, MaterialSe);
	quadratic=gluNewQuadric();
	gluQuadricNormals(quadratic, GLU_SMOOTH);
	gluQuadricTexture(quadratic, GL_TRUE);


	TextureImage[0] = auxDIBImageLoad("earth.bmp");
	glEnable(GL_TEXTURE_2D);
	glGenTextures(1, &texture);
	glBindTexture(GL_TEXTURE_2D, texture);


	glTexImage2D(GL_TEXTURE_2D, 0, 3, TextureImage[0]->sizeX,
		TextureImage[0]->sizeY, 0, GL_RGB, GL_UNSIGNED_BYTE, TextureImage[0]->data);
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
	free(TextureImage[0]->data);
	free(TextureImage[0]);
}
void changeSize(int w, int h) {
	float ratio = 1.0* w / h;
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	glViewport(0, 0, w, h);
	gluPerspective(45,ratio,1,100);
	glMatrixMode(GL_MODELVIEW);
}
char *textFileRead(char *fn) {
	FILE *fp;
	char *content = NULL;
	int count=0;
	if (fn != NULL) {
		fp = fopen(fn,"rt");
		if (fp != NULL) {
			fseek(fp, 0, SEEK_END);
			count = ftell(fp);
			rewind(fp);
			if (count > 0) {
				content = (char *)malloc(count+1);
				count = fread(content,1,count,fp);
				content[count] = '\0';
			} fclose(fp);
		}
	}
	return content;
}
GLuint v,f,p;
void setShaders() {
	char *vs = NULL,*fs = NULL,*fs2 = NULL;
	v = glCreateShader(GL_VERTEX_SHADER);
	f = glCreateShader(GL_FRAGMENT_SHADER);
	vs = textFileRead("vx.vert");
	fs = textFileRead("vx.frag");
	const char * vv = vs;
	const char * ff = fs;
	glShaderSource(v, 1, &vv,NULL);
	glShaderSource(f, 1, &ff,NULL);
	free(vs);free(fs);
	glCompileShader(v);
	glCompileShader(f);
	printShaderInfoLog(v);
	printShaderInfoLog(f);
	p = glCreateProgram();
	glAttachShader(p,v);
	glAttachShader(p,f);
	glLinkProgram(p);
	printProgramInfoLog(p);
	glUseProgram(p);
}

void printShaderInfoLog(GLuint obj) {
	int infologLength = 0;
	int charsWritten = 0;
	char *infoLog;
	glGetShaderiv(obj, GL_INFO_LOG_LENGTH,&infologLength);
	if (infologLength > 0) {
		infoLog = (char *)malloc(infologLength);
		glGetShaderInfoLog(obj, infologLength, &charsWritten,
			infoLog);
		printf("%s\n",infoLog);
		free(infoLog);
	}
}
void printProgramInfoLog(GLuint obj) {
	int infologLength = 0;
	int charsWritten = 0;
	char *infoLog;
	glGetProgramiv(obj, GL_INFO_LOG_LENGTH,&infologLength);
	if (infologLength > 0) {
		infoLog = (char *)malloc(infologLength);
		glGetProgramInfoLog(obj, infologLength, &charsWritten,
			infoLog);
		printf("%s\n",infoLog);
		free(infoLog);
	}
}
GLint texUnitLoc;
int _tmain(int argc, _TCHAR* argv[])
{
	char *argvv[] = {"hello ", " "};
	int argcc = 2; // must/should match the number of strings in argv
	glutInit(&argcc, argvv);
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE |
		GLUT_RGBA);
	glutCreateWindow("GLSL DEMO");
	init();
	glutDisplayFunc(renderScene);
	glutReshapeFunc(changeSize);
	glewInit();
	if (glewIsSupported("GL_VERSION_2_0"))
		printf("Ready for OpenGL 2.0\n");
	else {
		printf("OpenGL 2.0 not supported\n");
		exit(1);
	}
	setShaders();


	texUnitLoc = glGetUniformLocation(p, "tex");
	glUniform1i(texUnitLoc, 0);
	glutMainLoop();
	return 0;
}


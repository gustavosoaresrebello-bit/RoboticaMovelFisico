#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import String

def ler_e_publicar():
    # Inicializa o nó do sensor
    rospy.init_node('sensor_de_itens')
    
    # Cria o publicador que vai enviar mensagens de texto (String) no tópico /cor_do_item
    pub = rospy.Publisher('/cor_do_item', String, queue_size=10)
    
    # Dá um tempinho para o ROS registrar o tópico
    rospy.sleep(1)
    
    rospy.loginfo("=== SENSOR DE TRIAGEM ATIVADO ===")
    print("Cores disponíveis: 'vermelho', 'azul' ou 'verde'. Pressione Ctrl+C para sair.\n")
    
    while not rospy.is_shutdown():
        # Pede para o usuário digitar a cor no terminal
        cor_recebida = input("Digite a cor da caixa recebida: ").strip().lower()
        
        if cor_recebida in ['vermelho', 'azul', 'verde']:
            rospy.loginfo(f"Enviando ordem para o robô: Guardar item {cor_recebida.upper()}!")
            pub.publish(cor_recebida)
        else:
            print("⚠️ Cor não reconhecida no sistema. Tente: vermelho, azul ou verde.")

if __name__ == '__main__':
    try:
        ler_e_publicar()
    except rospy.ROSInterruptException:
        pass
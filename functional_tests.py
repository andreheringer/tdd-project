from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
class NewVisitorTest(unittest.TestCase):

    def setUp(self):  
         self.browser = webdriver.Firefox(executable_path="/home/andre/Projects/tdd-project/geckodriver")

    def tearDown(self):  
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self): 

        # Maria decidiu utilizar o novo app TODO. Ela entra em sua página principal:
        self.browser.get('http://127.0.0.1:8000')

        # Ela nota que o título da página menciona TODO
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text  
        self.assertIn('To-Do', header_text)

        # Ela é convidada a entrar com um item TODO imediatamente
        inputbox = self.browser.find_element_by_id('id_new_item')  
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # Ela digita "Estudar testes funcionais" em uma caixa de texto
        inputbox.send_keys('Estudar testes funcionais')

        # Quando ela aperta enter, a página atualiza, e mostra a lista
        # "1: Estudar testes funcionais" como um item da lista TODO
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')  
        self.assertIn('1: Estudar testes funcionais', [row.text for row in rows])
        
        # Ainda existe uma caixa de texto convidando para adicionar outro item
        # Ela digita: "Estudar testes de unidade"
        inputbox = self.browser.find_element_by_id('id_new_item')  
        inputbox.send_keys('Estudar testes de unidade')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # A página atualiza novamente, e agora mostra ambos os itens na sua lista
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Estudar testes funcionais', [row.text for row in rows])
        self.assertIn('2: Estudar testes de unidade', [row.text for row in rows])

        # Maria se pergunta se o site vai lembrar da sua lista. Então, ela verifica que
        # o site gerou uma URL única para ela -- existe uma explicação sobre essa feature

        # Ela visita a URL: a sua lista TODO ainda está armazenada

        # Satisfeita, ela vai dormir

if __name__ == '__main__':
    unittest.main()
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self): 

        # Maria decidiu utilizar o novo app TODO. Ela entra em sua página principal:
        self.browser.get(self.live_server_url)

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
        self.check_for_row_in_list_table('1: Estudar testes funcionais')
        
        # Ainda existe uma caixa de texto convidando para adicionar outro item
        # Ela digita: "Estudar testes de unidade"
        inputbox = self.browser.find_element_by_id('id_new_item')  
        inputbox.send_keys('Estudar testes de unidade')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # A página atualiza novamente, e agora mostra ambos os itens na sua lista
        self.check_for_row_in_list_table('1: Estudar testes funcionais')
        self.check_for_row_in_list_table('2: Estudar testes de unidade')
        # Maria se pergunta se o site vai lembrar da sua lista. Então, ela verifica que
        # o site gerou uma URL única para ela -- existe uma explicação sobre essa feature

        # Ela visita a URL: a sua lista TODO ainda está armazenada

        # Satisfeita, ela vai dormir

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:  
            try:
                table = self.browser.find_element_by_id('id_list_table')  
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return  
            except (AssertionError, WebDriverException) as e:  
                if time.time() - start_time > MAX_WAIT:  
                    raise e  
                time.sleep(0.5)
    
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Maria começa uma nova lista
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Estudar testes funcionais')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Estudar testes funcionais')

        # Ela nota que sua lista possui uma URL única
        maria_list_url = self.browser.current_url
        self.assertRegex(maria_list_url, '/lists/.+')

        # Agora, um novo usuário, João, entra no site
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # João visita a página inicial. Não existe nenhum sinal da lista de Maria
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Estudar testes funcionais', page_text)
        self.assertNotIn('2: Estudar testes de unidade', page_text)

        # João inicia uma nova lista
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Comprar leite')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Comprar leite')

        # João pega sua URL única
        joao_list_url = self.browser.current_url
        self.assertRegex(joao_list_url, '/lists/.+')
        self.assertNotEqual(joao_list_url, maria_list_url)

        # Novamente, não existe sinal da lista de Maria
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Estudar testes funcionais', page_text)
        self.assertIn('Comprar leite', page_text)

        # Satisfeitos, ambos vão dormir
    

from engine import Application
import pygame


class Application(Application):
    def __init__(self) -> None:
        super().__init__()

        ## TODO DEL RANDOM GEN
        import random
        TESTTAGS = ['A', "B", "C", "D"]
        TESTUTAGS = ['uA', "uB", "uC", "uD"]
        self.data = {
            'axis':(500, 500, 500),
            'stars':[
                {
                    'name': ''.join([random.choice("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm") for _ in range(random.randint(5, 10))]),
                    'pos':[random.randint(0, 500), random.randint(0, 500), random.randint(0, 500)],
                    'tags':[ _tag for _tag in TESTTAGS if random.randint(0, 2) == 0],
                    'data':[
                        {
                            'content': ''.join([random.choice("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm") for _ in range(random.randint(100, 200))]),
                            # 'usertags_whitelist':[ _tag for _tag in TESTTAGS if random.randint(0, 5) == 0],
                            # 'usertags_blacklist':[ _tag for _tag in TESTTAGS if random.randint(0, 5) == 0],
                        },
                    ],
                } for _ in range(100)
            ]
        }

        self.keybindings = {
            "quicksettings": pygame.K_q,
            # "quicksave": pygame.K_q,
        }
        

application = Application()
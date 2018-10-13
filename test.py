import snake
import visualize
import ai

if __name__ == "__main__":
    field_size = (30, 30)
    generation_size = 10
    surviver_count = 5 #the amount of fittest selected to breed the next generation
    child_per_survivor = generation_size // surviver_count
    mutation = 1

    generation = 1
    generations=[]
    for i in range(generation_size):
        game = snake.Game(field_size, snake.Snake(snake.Vector(14, 14), snake.Vector.UP, 3))
        model = ai.create_model(field_size)
        generations.append((model, game))

    vis = visualize.Visualizer((600, 450), "Snake", 5, (255, 0, 0), (0, 255, 0))

    last_update = 0
    update_frequency = 200
    max_ticks = 50
    tick_count = 0
    dead = 0

    while vis.running:
        vis.begin_frame()
        for i in range(len(generations)): #display fields
            x = i % 4
            y = i // 4
            vis.draw_field(generations[i][1].field, (x * field_size[0] * 5, y * field_size[1] * 5))
        vis.end_frame()

        ticks = vis.get_ticks()
        if ticks >= last_update + update_frequency: #update games
            if tick_count < max_ticks and dead < len(generations): #check if any snakes are still alive or if time ran out
                for entity in generations:
                    if entity[1].running:
                        command = ai.get_command(entity[0], entity[1].field)
                        entity[1].update(command)
                        if not entity[1].running: #snake died during this move
                            dead += 1
                last_update = ticks
                tick_count += 1
            else: #new generation
                print("Finished Generation ", generation)
                tick_count = 0
                dead = 0

                print("Evaluating generation ", generation)
                best = ai.get_best(generations, surviver_count)

                generation += 1
                print("Generation: ", generation)
                new_generation = []
                for survivor in best:
                    for i in range(child_per_survivor):
                        model = ai.mutate_model(survivor[1][0], mutation)
                        game = snake.Game(field_size, snake.Snake(snake.Vector(14, 14), snake.Vector.UP, 3))
                        new_generation.append((model, game))
                generations = new_generation



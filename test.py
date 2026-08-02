# PythonECS - Test

# ================================================================================================ #
# Imports

from dataclasses import dataclass

from EntityComponentSystem import *

# ================================================================================================ #
# Components

@dataclass
class Position:
	x: float
	y: float

@dataclass
class Velocity:
	dx: float
	dy: float

@dataclass
class Health:
	value: int

# ================================================================================================ #
# Resources

@dataclass
class DeltaTime:
	dt: float

@dataclass
class DamageEvent:
	target_entity: int
	amount: int

# ================================================================================================ #
# Systems

def setup_system(ecs: EntityComponentSystem) -> None:
	print("🚀 [STARTUP] Initializing Game Entities...")
	ecs.set_resource(DeltaTime(dt=0.016))

	# Spawn Player
	player = ecs.create_entity()
	ecs.add_component(player, Position(0, 0))
	ecs.add_component(player, Velocity(10, 5))
	ecs.add_component(player, Health(100))

	# Spawn Weapon (Attached as child to Player)
	weapon = ecs.create_entity()
	ecs.add_component(weapon, Position(0, 0))
	ecs.set_parent(child=weapon, parent=player)

def movement_system(ecs: EntityComponentSystem) -> None:
	dt = ecs.get_resource(DeltaTime).dt
	for entity, pos, vel in ecs.query(Position, Velocity):
		pos.x += vel.dx * dt
		pos.y += vel.dy * dt
		print(f"🏃 [UPDATE] Entity {entity} moved to ({pos.x:.2f}, {pos.y:.2f})")

	# Trigger a dummy event for demonstration
	ecs.events.send(DamageEvent(target_entity=0, amount=25))

def combat_system(ecs: EntityComponentSystem) -> None:
	for event in ecs.events.read(DamageEvent):
		if ecs.has_component(event.target_entity, Health):
			hp = ecs.get_component(event.target_entity, Health)
			hp.value -= event.amount
			print(f"⚔️  [POST_UPDATE] Entity {event.target_entity} took {event.amount} damage! HP left: {hp.value}")

def render_system(ecs: EntityComponentSystem) -> None:
	# Use observer to detect new entities
	newly_positioned = ecs.get_added(Position)
	if newly_positioned:
		print(f"🎨 [RENDER] New entities with Position added this frame: {newly_positioned}")

# ================================================================================================ #
# Entry Point

if __name__ == "__main__":
	ecs = EntityComponentSystem()

	# Register Systems to Stages
	ecs.add_system(setup_system, Stage.STARTUP)
	ecs.add_system(movement_system, Stage.UPDATE)
	ecs.add_system(combat_system, Stage.POST_UPDATE)
	ecs.add_system(render_system, Stage.RENDER)

	print("--- Frame 1 ---")
	ecs.update()

	print("\n--- Frame 2 ---")
	ecs.update()
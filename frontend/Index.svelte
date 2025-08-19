<svelte:options accessors={true} />

<script lang="ts">
	import { Block, BlockTitle } from "@gradio/atoms";
	import type { LoadingStatus } from "@gradio/statustracker";
	import { StatusTracker } from "@gradio/statustracker";
	import type { Gradio } from "@gradio/utils";

	export let gradio: Gradio<{
		change: {
			video: { id: string; src: string; start: number; duration: number }[];
			audio: { id: string; src: string; start: number; duration: number; lane: number }[];
		};
		clear_status: LoadingStatus;
	}>;
	export let label = "Timeline";
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: {
		video: { id: string; src: string; start: number; duration: number }[];
		audio: { id: string; src: string; start: number; duration: number; lane: number }[];
	} | null = null;
	export let show_label: boolean;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus | undefined = undefined;
	export let interactive: boolean;

	let video_element: HTMLVideoElement;
	let audio_elements: Record<string, HTMLAudioElement> = {};
	let playing = false;
	let currentTime = 0;
	let timeline_width = 800;
	const PIXELS_PER_SECOND = 50;

	let duration = 0;
	let animation_frame_id: number;

	$: if (value && value.video && value.video.length > 0) {
		duration = value.video.reduce((max, v) => Math.max(max, v.start + v.duration), 0);
		timeline_width = duration * PIXELS_PER_SECOND;
	} else {
		duration = 0;
		timeline_width = 800;
	}

	function handle_change(): void {
		if (value) {
			gradio.dispatch("change", value);
		}
	}

	function handle_audio_metadata(audio_item_id: string) {
		if (!value) return;
		const audio_el = audio_elements[audio_item_id];
		const audio_item = value.audio.find(i => i.id === audio_item_id);

		if (audio_el && audio_item && audio_el.duration !== Infinity) {
			if (audio_item.duration !== audio_el.duration) {
				audio_item.duration = audio_el.duration;
				value = { ...value }; // trigger reactivity
				handle_change();
			}
		}
	}

	let last_time = 0;
	function play_loop(timestamp: number) {
		if (!playing) return;

		if (last_time) {
			const delta = (timestamp - last_time) / 1000;
			currentTime += delta;
		}
		last_time = timestamp;

		if (currentTime > duration) {
			currentTime = 0;
			playing = false;
			last_time = 0;
		}

		handle_time_update();
		animation_frame_id = requestAnimationFrame(play_loop);
	}

	function toggle_play() {
		playing = !playing;
		if (playing) {
			last_time = 0;
			animation_frame_id = requestAnimationFrame(play_loop);
		} else {
			cancelAnimationFrame(animation_frame_id);
			if (video_element) video_element.pause();
			Object.values(audio_elements).forEach(a => a.pause());
		}
	}

	let active_video_item_id: string | null = null;

	function handle_time_update() {
		if (!value) return;

		// Video
		const current_video_item = value.video.find(
			v => currentTime >= v.start && currentTime < v.start + v.duration
		);

		if (current_video_item) {
			if (active_video_item_id !== current_video_item.id) {
				active_video_item_id = current_video_item.id;
				if (video_element) {
					video_element.src = current_video_item.src;
				}
			}
			if (video_element) {
				const desired_time = currentTime - current_video_item.start;
				if (Math.abs(video_element.currentTime - desired_time) > 0.2) {
					video_element.currentTime = desired_time;
				}
				if (video_element.paused && playing) {
					video_element.play();
				}
			}
		} else {
			active_video_item_id = null;
			if (video_element && !video_element.paused) {
				video_element.pause();
			}
		}

		// Audio
		for (const audio_item of value.audio) {
			const audio_el = audio_elements[audio_item.id];
			if (audio_el) {
				const should_be_playing = currentTime >= audio_item.start && currentTime < (audio_item.start + audio_item.duration);

				if (should_be_playing) {
					const desired_time = currentTime - audio_item.start;
					if (Math.abs(audio_el.currentTime - desired_time) > 0.2) {
						audio_el.currentTime = desired_time;
					}
					if (audio_el.paused && !audio_el.ended && playing) {
						audio_el.play();
					}
				} else {
					if (!audio_el.paused) {
						audio_el.pause();
						audio_el.currentTime = 0;
					}
				}
			}
		}
	}

	function handle_seek(event: MouseEvent) {
		if (!duration) return;
		const timeline_element = event.currentTarget as HTMLDivElement;
		const rect = timeline_element.getBoundingClientRect();
		const x = event.clientX - rect.left;
		const new_time = (x / timeline_width) * duration;
		currentTime = new_time;
		if (!playing) {
			handle_time_update();
		}
	}

	let dragged_item: { type: 'audio' | 'video', index: number } | null = null;
	let drag_start_x = 0;
	let original_start = 0;

	function handle_drag_start(event: DragEvent, type: 'audio' | 'video', index: number) {
		if (is_resizing) {
			event.preventDefault();
			return;
		}
		dragged_item = { type, index };
		drag_start_x = event.clientX;
		if (value) {
			if (type === 'video') {
				original_start = value.video[index].start;
			} else {
				original_start = value.audio[index].start;
			}
		}
		if (event.dataTransfer) {
			event.dataTransfer.effectAllowed = "move";
		}
	}

	function handle_drop(event: DragEvent) {
		if (!dragged_item || !value) return;
		event.preventDefault();

		const dx = event.clientX - drag_start_x;
		const dt = dx / PIXELS_PER_SECOND;

		if (dragged_item.type === 'video') {
			const item = value.video[dragged_item.index];
			item.start = Math.max(0, original_start + dt);
		} else {
			const item = value.audio[dragged_item.index];
			item.start = Math.max(0, original_start + dt);
		}

		dragged_item = null;
		handle_change();
		// Force re-render
		value = { ...value };
	}

	function handle_drag_over(event: DragEvent) {
		event.preventDefault();
	}

	let is_resizing = false;
	let resizing_item: { type: 'audio' | 'video', index: number } | null = null;
	let resize_start_x = 0;
	let original_duration = 0;

	function handle_resize_start(event: MouseEvent, type: 'audio' | 'video', index: number) {
		event.stopPropagation();
		is_resizing = true;
		resizing_item = { type, index };
		resize_start_x = event.clientX;
		if (value) {
			if (type === 'video') {
				original_duration = value.video[index].duration;
			} else {
				original_duration = value.audio[index].duration;
			}
		}
		window.addEventListener('mousemove', handle_resize_move);
		window.addEventListener('mouseup', handle_resize_end);
	}

	function handle_resize_move(event: MouseEvent) {
		if (!resizing_item || !value) return;

		const dx = event.clientX - resize_start_x;
		const d_duration = dx / PIXELS_PER_SECOND;

		if (resizing_item.type === 'video') {
			const item = value.video[resizing_item.index];
			item.duration = Math.max(0.1, original_duration + d_duration);
		} else {
			const item = value.audio[resizing_item.index];
			item.duration = Math.max(0.1, original_duration + d_duration);
		}
		value = { ...value };
	}

	function handle_resize_end() {
		if (!resizing_item) return;
		resizing_item = null;
		window.removeEventListener('mousemove', handle_resize_move);
		window.removeEventListener('mouseup', handle_resize_end);
		handle_change();
		is_resizing = false;
	}

	function handle_item_double_click(start_time: number) {
		currentTime = start_time;
		if (!playing) {
			handle_time_update();
		}
	}

	function handle_keydown(event: KeyboardEvent) {
		if (event.key === ' ') {
			event.preventDefault();
			toggle_play();
		} else if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
			event.preventDefault();
			const scrub_amount = 1; // 1 second
			if (event.key === 'ArrowLeft') {
				currentTime = Math.max(0, currentTime - scrub_amount);
			} else {
				currentTime = Math.min(duration, currentTime + scrub_amount);
			}
			if (!playing) {
				handle_time_update();
			}
		} else if (event.key === 'Backspace' || event.key.toLowerCase() === 'w') {
			event.preventDefault();
			currentTime = 0;
			if (!playing) {
				handle_time_update();
			}
		}
	}
</script>

<svelte:window on:keydown={handle_keydown} />

<Block
	{visible}
	{elem_id}
	{elem_classes}
	{scale}
	{min_width}
	allow_overflow={false}
	padding={true}
>
	{#if loading_status}
		<StatusTracker
			autoscroll={gradio.autoscroll}
			i18n={gradio.i18n}
			{...loading_status}
			on:clear_status={() => gradio.dispatch("clear_status", loading_status)}
		/>
	{/if}

	<div class="timeline-container">
		<BlockTitle {show_label} info={undefined}>{label}</BlockTitle>

		<div class="sticky-pane">
			<div class="controls">
				<button on:click={toggle_play}>{playing ? 'Pause' : 'Play'}</button>
			</div>

			<video
				bind:this={video_element}
				style="width: 400px; height: 225px; margin-bottom: 10px; background: black;"
				class:visible={active_video_item_id !== null}
				muted
			></video>
		</div>

		{#if value && value.audio}
			{#each value.audio as audio_item (audio_item.id)}
				<audio
					bind:this={audio_elements[audio_item.id]}
					src={audio_item.src}
					on:loadedmetadata={() => handle_audio_metadata(audio_item.id)}
				></audio>
			{/each}
		{/if}

		<div class="timeline" style="width: {timeline_width}px" on:click={handle_seek} on:drop={handle_drop} on:dragover={handle_drag_over}>
			<div class="playhead" style="left: {duration > 0 ? (currentTime / duration) * 100 : 0}%"></div>

			<!-- Video Track -->
			<div class="track video-track">
				{#if value && value.video}
					{#each value.video as item, i (item.id)}
						<div
							class="item video-item"
							style="left: {item.start * PIXELS_PER_SECOND}px; width: {item.duration * PIXELS_PER_SECOND}px;"
							draggable={interactive}
							on:dragstart={(e) => handle_drag_start(e, 'video', i)}
							on:dblclick={() => handle_item_double_click(item.start)}
						>
							{item.id}
							{#if interactive}
								<div class="resize-handle" on:mousedown={(e) => handle_resize_start(e, 'video', i)}></div>
							{/if}
						</div>
					{/each}
				{/if}
			</div>

			<!-- Audio Tracks -->
			{#if value && value.audio}
				{@const max_lane = value.audio.reduce((max, item) => Math.max(max, item.lane), -1)}
				{#each Array(max_lane + 1) as _, lane_idx}
					<div class="track audio-track">
						{#each value.audio.filter(item => item.lane === lane_idx) as item, i (item.id)}
							{@const original_index = value.audio.findIndex(a => a.id === item.id)}
							<div
								class="item audio-item"
								style="left: {item.start * PIXELS_PER_SECOND}px; width: {item.duration * PIXELS_PER_SECOND}px;"
								draggable={interactive}
								on:dragstart={(e) => handle_drag_start(e, 'audio', original_index)}
								on:dblclick={() => handle_item_double_click(item.start)}
							>
								{item.id}
								{#if interactive}
									<div class="resize-handle" on:mousedown={(e) => handle_resize_start(e, 'audio', original_index)}></div>
								{/if}
							</div>
						{/each}
					</div>
				{/each}
			{/if}
		</div>
	</div>
</Block>

<style>
	.timeline-container {
		width: 100%;
		overflow-x: auto;
		background-color: #f7f9fc;
		padding: 1rem;
		border-radius: 0.5rem;
		position: relative;
	}
	.sticky-pane {
		position: sticky;
		left: 0;
		background: #f7f9fc;
		z-index: 20;
		width: 400px;
	}
	.timeline {
		position: relative;
		background: #ffffff;
		height: auto;
		min-height: 100px;
		border: 1px solid #e0e0e0;
		border-radius: 0.5rem;
		overflow: hidden;
	}
	.track {
		position: relative;
		height: 50px;
		box-sizing: border-box;
	}
	.track:not(:last-child) {
		border-bottom: 1px solid #e0e0e0;
	}
	.video-track {
		background-color: rgba(71, 145, 255, 0.1);
	}
	.audio-track {
		background-color: rgba(0, 200, 83, 0.1);
	}
	.item {
		position: absolute;
		height: 36px;
		top: 7px;
		border-radius: 0.25rem;
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: move;
		font-size: 0.8rem;
		font-weight: 500;
		box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
		transition: all 0.2s ease-in-out;
		overflow: hidden;
		white-space: nowrap;
		text-overflow: ellipsis;
		padding: 0 0.5rem;
	}
	.item:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 8px rgba(0,0,0,0.15), 0 3px 6px rgba(0,0,0,0.20);
	}
	.video-item {
		background: linear-gradient(45deg, #4791ff, #2d77d9);
		border: 1px solid #2d77d9;
	}
	.audio-item {
		background: linear-gradient(45deg, #00c853, #00a042);
		border: 1px solid #00a042;
	}
	.resize-handle {
		position: absolute;
		right: 0;
		top: 0;
		width: 6px;
		height: 100%;
		cursor: ew-resize;
		background: rgba(255, 255, 255, 0.2);
	}
	.playhead {
		position: absolute;
		width: 2px;
		height: 100%;
		background: #4791ff;
		top: 0;
		z-index: 10;
		box-shadow: 0 0 5px #4791ff;
	}
	.controls {
		margin-bottom: 1rem;
	}
	.controls button {
		background-color: #4791ff;
		color: white;
		border: none;
		padding: 0.5rem 1rem;
		border-radius: 0.25rem;
		font-size: 0.9rem;
		cursor: pointer;
		transition: background-color 0.2s;
	}
	.controls button:hover {
		background-color: #2d77d9;
	}
	video:not(.visible) {
		visibility: hidden;
	}
</style>

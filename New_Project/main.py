from graph.workflow import build_graph
import uuid
import json

def main():
    graph = build_graph()
    ticker = "TSLA"

    # The thread ID is critical. It acts as the memory key for this specific execution
    thread_id = str(uuid.uuid4())

    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "ticker": ticker,
        "messages": []
    }

    print(f"🚀 Starting Research Workflow for {ticker}...\n")

    #1. Run the graph untill it hits interupt
    for event in graph.stream(initial_state, config = config):
        for node_name, state_update in event.items():
            pass #Logging is handled inside the agents

    #2. Fetch the current state at the pause
    current_state = graph.get_state(config)
    
    # Check if the graph is currently paused
    if current_state.next:
        print("\n=======================================================")
        print(" ⚠️  HUMAN-IN-THE-LOOP CHECKPOINT: CIO REVIEW REQUIRED  ")
        print("=======================================================\n")

        state_data = current_state.values
        print("--- FUNDAMENTAL PREVIEW ---")
        # pyrefly: ignore [unsupported-operation]
        print(state_data.get("fundamental_analysis")[:300] + "...\n")
        print("--- TECHNICAL PREVIEW ---")
        # pyrefly: ignore [unsupported-operation]
        print(state_data.get("technical_analysis")[:300] + "...\n")

        #3. Wait for user input to proceed
        user_approval = input("Do you want to approve the trade and continue to portfolio construction? (yes/no): ").strip().lower()

        if user_approval == "yes":
            #4. Resume the graph
            print("\n✅ Proceeding to Portfolio Optimization...")
            for event in graph.stream(None, config=config, stream_mode="values"):
                pass
            final_state = graph.get_state(config)
            print("\n=======================================================")
            print("                FINAL INVESTMENT MEMO                  ")
            print("=======================================================\n")
            print(final_state.values.get("final_memo"))
        else:
            print("\n❌ Workflow cancelled by user.")
    else:
        print("Workflow completed without interruptions.")

if __name__ == "__main__":
    main()
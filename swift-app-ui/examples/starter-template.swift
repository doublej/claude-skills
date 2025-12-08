import SwiftUI

// MARK: - App Entry Point
@main
struct ExampleApp: App {
  var body: some Scene {
    WindowGroup {
      ContentView()
    }
  }
}

// MARK: - Main Content View
struct ContentView: View {
  @State private var isLoading = false
  @State private var selectedTab = 0

  var body: some View {
    TabView(selection: $selectedTab) {
      HomeView()
        .tabItem {
          Label("Home", systemImage: "house.fill")
        }
        .tag(0)

      ExploreView()
        .tabItem {
          Label("Explore", systemImage: "magnifyingglass")
        }
        .tag(1)

      ProfileView()
        .tabItem {
          Label("Profile", systemImage: "person.fill")
        }
        .tag(2)
    }
  }
}

// MARK: - Home Screen
struct HomeView: View {
  @State private var items: [Item] = []
  @State private var isLoading = true

  var body: some View {
    NavigationStack {
      ZStack {
        // Background
        LinearGradient(
          gradient: Gradient(colors: [
            Color("BackgroundPrimary"),
            Color("BackgroundSecondary")
          ]),
          startPoint: .topLeading,
          endPoint: .bottomTrailing
        )
        .ignoresSafeArea()

        // Content
        ScrollView {
          VStack(spacing: 20) {
            // Header
            VStack(alignment: .leading, spacing: 8) {
              Text("Welcome Back")
                .font(.system(size: 28, weight: .bold, design: .default))
                .tracking(0.3)

              Text("Explore what's new")
                .font(.system(size: 16, weight: .regular, design: .default))
                .foregroundColor(.secondary)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.horizontal, 16)
            .padding(.vertical, 20)

            // Items Grid
            VStack(spacing: 12) {
              if isLoading {
                LoadingView()
              } else if items.isEmpty {
                EmptyStateView()
              } else {
                ForEach(items) { item in
                  ItemCardView(item: item)
                }
              }
            }
            .padding(.horizontal, 16)
            .padding(.bottom, 20)
          }
        }
      }
      .navigationTitle("Home", displayMode: .inline)
      .task {
        await loadItems()
      }
    }
  }

  @MainActor
  private func loadItems() async {
    isLoading = true
    try? await Task.sleep(nanoseconds: 1_000_000_000) // Simulate network delay
    items = Item.samples
    isLoading = false
  }
}

// MARK: - Item Card Component
struct ItemCardView: View {
  let item: Item

  var body: some View {
    VStack(alignment: .leading, spacing: 12) {
      // Image/Icon
      RoundedRectangle(cornerRadius: 12)
        .fill(item.color.opacity(0.2))
        .frame(height: 120)
        .overlay(
          Image(systemName: item.icon)
            .font(.system(size: 40))
            .foregroundColor(item.color)
        )

      // Content
      VStack(alignment: .leading, spacing: 8) {
        HStack {
          VStack(alignment: .leading, spacing: 4) {
            Text(item.title)
              .font(.headline)
              .lineLimit(1)

            Text(item.description)
              .font(.caption)
              .foregroundColor(.secondary)
              .lineLimit(2)
          }

          Spacer()

          if item.isNew {
            BadgeView(text: "New", color: item.color)
          }
        }

        // Action Button
        Button(action: {}) {
          Text("View Details")
            .font(.subheadline)
            .fontWeight(.semibold)
            .frame(maxWidth: .infinity)
            .frame(height: 36)
            .background(item.color.opacity(0.1))
            .foregroundColor(item.color)
            .cornerRadius(8)
        }
        .accessibilityLabel("View details for \(item.title)")
      }
      .padding(12)
    }
    .background(Color("CardBackground"))
    .cornerRadius(16)
    .shadow(color: Color.black.opacity(0.08), radius: 8, x: 0, y: 2)
  }
}

// MARK: - Badge Component
struct BadgeView: View {
  let text: String
  let color: Color

  var body: some View {
    Text(text)
      .font(.caption2)
      .fontWeight(.semibold)
      .foregroundColor(.white)
      .padding(.horizontal, 8)
      .padding(.vertical, 4)
      .background(color)
      .cornerRadius(4)
  }
}

// MARK: - Loading State
struct LoadingView: View {
  var body: some View {
    VStack(spacing: 12) {
      ForEach(0..<3, id: \.self) { _ in
        SkeletonItemCard()
      }
    }
    .redacted(reason: .placeholder)
    .shimmering()
  }
}

struct SkeletonItemCard: View {
  var body: some View {
    VStack(alignment: .leading, spacing: 12) {
      RoundedRectangle(cornerRadius: 12)
        .fill(Color.gray.opacity(0.2))
        .frame(height: 120)

      VStack(alignment: .leading, spacing: 8) {
        RoundedRectangle(cornerRadius: 4)
          .fill(Color.gray.opacity(0.2))
          .frame(height: 16)

        RoundedRectangle(cornerRadius: 4)
          .fill(Color.gray.opacity(0.2))
          .frame(height: 12)
      }
      .padding(12)
    }
    .background(Color("CardBackground"))
    .cornerRadius(16)
  }
}

extension View {
  func shimmering() -> some View {
    modifier(ShimmeringModifier())
  }
}

struct ShimmeringModifier: ViewModifier {
  @State private var isShimmering = false

  func body(content: Content) -> some View {
    ZStack {
      content
        .opacity(isShimmering ? 0.6 : 1)

      LinearGradient(
        gradient: Gradient(colors: [.clear, .white.opacity(0.3), .clear]),
        startPoint: .topLeading,
        endPoint: .bottomTrailing
      )
      .offset(x: isShimmering ? 400 : -400)
    }
    .onAppear {
      withAnimation(.linear(duration: 1.5).repeatForever(autoreverses: false)) {
        isShimmering = true
      }
    }
  }
}

// MARK: - Empty State
struct EmptyStateView: View {
  var body: some View {
    VStack(spacing: 16) {
      Image(systemName: "list.bullet.circle")
        .font(.system(size: 48))
        .foregroundColor(.secondary)

      VStack(spacing: 4) {
        Text("No Items")
          .font(.headline)

        Text("Items will appear here")
          .font(.caption)
          .foregroundColor(.secondary)
      }

      Button(action: {}) {
        Text("Create Item")
          .fontWeight(.semibold)
          .padding(.horizontal, 20)
          .padding(.vertical, 10)
          .background(Color("AccentColor"))
          .foregroundColor(.white)
          .cornerRadius(8)
      }
    }
    .padding(32)
  }
}

// MARK: - Explore View
struct ExploreView: View {
  var body: some View {
    NavigationStack {
      Text("Explore View")
        .navigationTitle("Explore", displayMode: .inline)
    }
  }
}

// MARK: - Profile View
struct ProfileView: View {
  var body: some View {
    NavigationStack {
      Text("Profile View")
        .navigationTitle("Profile", displayMode: .inline)
    }
  }
}

// MARK: - Data Models
struct Item: Identifiable {
  let id = UUID()
  let title: String
  let description: String
  let icon: String
  let color: Color
  let isNew: Bool

  static let samples = [
    Item(title: "Swift Basics", description: "Learn SwiftUI fundamentals", icon: "swift", color: .orange, isNew: true),
    Item(title: "Design System", description: "Build consistent interfaces", icon: "paintpalette.fill", color: .blue, isNew: false),
    Item(title: "Performance", description: "Optimize your app", icon: "speedometer", color: .green, isNew: true),
  ]
}

// MARK: - Preview
#Preview {
  ContentView()
    .preferredColorScheme(.light)
}

#Preview("Dark Mode") {
  ContentView()
    .preferredColorScheme(.dark)
}

#Preview("Large Text") {
  ContentView()
    .environment(\.dynamicTypeSize, .xLarge)
}
